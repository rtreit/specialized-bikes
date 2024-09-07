from django.db import models

# Create your models here.
class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class OutgoingRequest(TimeStampedModel):
    url = models.TextField(default="")
    method = models.CharField(max_length=10, default="")
    response = models.TextField(default="")
    payload = models.TextField(default="")
    status_code = models.IntegerField()

class Error(TimeStampedModel):
    message = models.TextField()
    stack_trace = models.TextField()