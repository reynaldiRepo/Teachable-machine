from django.db import models

# Create your models here.

class Machine (models.Model):
    Name = models.CharField(max_length=255)
    Created = models.DateTimeField()

class MachineClass (models.Model):
    Name = models.CharField(max_length=255)
    