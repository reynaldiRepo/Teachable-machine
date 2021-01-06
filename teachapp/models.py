from django.db import models

# Create your models here.

class Machine (models.Model):
    Name = models.CharField(max_length=255)
    Created = models.DateTimeField()
    Directory = models.CharField(max_length=255, default="")
    #machine setting data
    epoch = models.CharField(max_length=255, default="")
    batch = models.CharField(max_length=255, default="")
    learningrate = models.CharField(max_length=255, default="")

class MachineClass (models.Model):
    Name = models.CharField(max_length=255)
    Machine_ID = models.CharField(max_length=255, default="0")
    