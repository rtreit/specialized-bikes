from django.contrib import admin

from .models import OutgoingRequest, Error

# Register your models here.

class OutgoingRequestAdmin(admin.ModelAdmin):
    list_display = ('url','method','status_code','created_at', 'request_number')
    list_filter = ('status_code',)

    def request_number(self, obj):
        return obj.id
    request_number.short_description = "Request #"

admin.site.register(OutgoingRequest, OutgoingRequestAdmin)

class ErrorAdmin(admin.ModelAdmin):
    list_display = ('created_at', 'id')

admin.site.register(Error, ErrorAdmin)

