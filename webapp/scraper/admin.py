from django.contrib import admin
from django.utils.safestring import mark_safe
from .models import SpecializedBike

# Register your models here.


class SpecializedBikeAdmin(admin.ModelAdmin):
    readonly_fields = ("created_at", "updated_at", "bike_url", "id")
    list_display = ("name", "bike_class", "type", "price", "bike_url", "created_at")
    list_filter = ("bike_class", "type")
    search_fields = ("name", "size", "bike_class", "type", "subtype")
    ordering = ("-price",)

    def bike_url(self, obj):
        return mark_safe(f'<a href="{obj.url}" target="_blank">{obj.url}</a>')


admin.site.register(SpecializedBike, SpecializedBikeAdmin)
