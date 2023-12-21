import os
import json
import requests
from datetime import datetime
from dotenv import load_dotenv
from django.db import models
from django.contrib.auth import get_user_model
from django.core.exceptions import PermissionDenied, BadRequest

load_dotenv()

CustomUser = get_user_model()


MAX_ATTEMPT = 5

VERIFICATION_STATES = [
	(0, 'Initiated'),
	(1, 'Approved'), 
	(-1, 'Rejected'),
]

def get_sentinel_user():
	#The first created super user becomes the default control staff of any verification process.
	return CustomUser.objects.filter(is_superuser=True).order_by('id').first()


def verify_user_id(id_type, data):
	endpoints = {
		"nin": os.getenv("NIN_VERIFICATION_ENDPOINT"),
		"passport": os.getenv("PASSPORT_VERIFICATION_ENDPOINT"),
		"bvn": os.getenv("BVN_VERIFICATION_ENDPOINT"),
	}

	headers = {
		"token": os.getenv("YOUVERIFY_SECRET"),
		"Content-Type": "application/json"
	}

	data = json.dumps(data)
	endpoint = endpoints[id_type]

	try:
		response = requests.post(endpoint, headers=headers, data=data)
		return response.json()

	except requests.exceptions.RequestException as e:
		# Handle request errors
		print(f"Request to {endpoint} failed: {e}")
		return False


class Verification(models.Model):
	user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
	status = models.SmallIntegerField(
		default=0, 
		choices=VERIFICATION_STATES
	)
	id_number = models.CharField(max_length=15, null=False, unique=True)
	metadata = models.JSONField(default=dict, blank=True)
	attempt = models.SmallIntegerField(default=1)
	submitted_on = models.DateTimeField(auto_now_add=True)
	last_updated_on = models.DateTimeField(auto_now=True)

	def verification_payload(self, ):
		return {
			"id": self.id_number,
			"metadata": {
				"user_email": self.user.email
			},
			"isSubjectConsent": "true",
			"validations": {
				"data": {
					"lastName": self.user.last_name,
				},
			}
		}

	def check_verification_result(self, result):
		if result['success']:
			self.attempt = self.attempt + 1
			if result['data']['status'] == "found" and result['data']['allValidationPassed']:
				self.status = 1 #Validated
				self.metadata = result['data']['validations']

				return True
			else:
				self.status = -1 #Rejected
				self.metadata = {
					"rejection_reason": result['data']['validations']['validationMessages']
				}
		else:
			if result["name"] == "ValidationError":
				self.status = -1 #Rejected
				self.attempt = self.attempt + 1
				self.metadata = {
					"rejection_reason": result['message']
				}

		return False

	def user_can_verify(self, ):
		'''
			1. User cannot verify if verification has already been verified.
			2. User cannot attempt a verification more than MAX_ATTEMPT times.
		'''
		if self.status == 1:
			return (False, "Already verified.")

		if self.attempt >= MAX_ATTEMPT:
			return (False, "Verification attempt limit reached.")

		return (True, "User can verify.")

	class Meta:
		abstract = True


class ID_Verification(Verification):
	ID_VERIFICATION_METHODS = [
		('passport', 'International Passport'), 
		('nin', 'National Identification')
	]
	
	method = models.CharField(max_length=20, choices=ID_VERIFICATION_METHODS)
	id_document = models.FileField(upload_to='verification_documents/', null=True)
	review_notes = models.TextField(blank=True, null=True)
	
	def __str__(self):
		return f"{self.user.username} - {self.status}"

	def verify_id(self, ):

		data = self.verification_payload()

		document_path = "https://i.ibb.co/twfVGqj/download.jpg"
		# document_path = self.id_document.path

		if self.method == 'nin':
			data["validations"]["selfie"] = {
				"image": document_path
			}

		if self.method == 'passport':
			data["lastName"] = self.user.last_name
			data["validations"] = {
				"selfie": {
					"image": document_path
				}
			}
		
		result = verify_user_id(self.method, data)
		if result:
			self.check_verification_result(result)

	def save(self, *args, **kwargs):
		'''
			1. Make sure selfie is uploaded (id_document) before initiating any verification
		'''
		can_verify = self.user_can_verify()
		if can_verify[0]:
			if self.id_document is None:
				super().save(*args, **kwargs)

			self.verify_id()
			super().save(*args, **kwargs)
		else:
			raise BadRequest(can_verify[1])



class BVN_Verification(Verification):

	def __str__(self):
		return f"{self.user.username} - {self.status}"

	def verify_bvn(self, ):
		# Make a request to a specific endpoint
		data = self.verification_payload()
		data["validations"]["data"]["dateOfBirth"] = self.user.date_of_birth.strftime('%Y-%m-%d')

		result = verify_user_id('bvn', data)

		if result:
			self.check_verification_result(result)


	def save(self, *args, **kwargs):
		can_verify = self.user_can_verify()
		if can_verify[0]:
			self.verify_bvn()
			# Continue with the normal save process
			super().save(*args, **kwargs)
		else:
			raise BadRequest(can_verify[1])