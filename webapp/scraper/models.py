from django.db import models


class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


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
