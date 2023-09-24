from django.db import models
from uuid import uuid4

# Create your models here.

class Message(models.Model):
    id = models.AutoField(primary_key=True)
    content = models.TextField(max_length=2500, blank=False)
    timestamp = models.DateTimeField(auto_now=True)
    
    
class Room(models.Model):
    room_id = models.CharField(max_length=100, blank=False, null=False)
    room_password = models.CharField(max_length=500, null=False, blank=False)
    messages = models.ManyToManyField(Message, null=True, blank=True)
    