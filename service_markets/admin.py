from django.contrib import admin
from .models import BaseAsset, Asset, Market

class MarketAdmin(admin.ModelAdmin):
	list_display = ('asset', 'value', 'timestamp', 'change_direction')
	
	def get_readonly_fields(self, request, obj=None):
		# If obj is None, it's a new object being created, so allow editing.
		if obj is None:
			return []
		# If obj exists, it's an existing object, so make all fields readonly.
		return [field.name for field in obj._meta.fields]

admin.site.register(Market, MarketAdmin)
admin.site.register(Asset)
admin.site.register(BaseAsset)
