from django.db import models

from core.models import TimeStampedModel

class SpecializedBike(TimeStampedModel):
    name = models.CharField(max_length=255, blank=True, null=True, default="")
    size = models.CharField(max_length=255, blank=True, null=True, default="")
    bike_class = models.CharField(max_length=255, blank=True, null=True, default="")
    type = models.CharField(max_length=255, blank=True, null=True, default="")
    subtype = models.CharField(max_length=255, blank=True, null=True, default="")
    price = models.FloatField(blank=True, null=True, default=None)
    url = models.URLField()

    def __str__(self):
        return self.name
