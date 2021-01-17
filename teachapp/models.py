from django.db import models
from zipfile import ZipFile
import os
from django import conf
from django.contrib.auth.models import User

# Create your models here.

class Machine (models.Model):
    Name = models.CharField(max_length=255)
    Created = models.DateTimeField()
    Directory = models.CharField(max_length=255, default="")
    #machine setting data
    epoch = models.CharField(max_length=255, default="")
    batch = models.CharField(max_length=255, default="")
    learningrate = models.CharField(max_length=255, default="")
    User = models.CharField(max_length=255, default="")

    def getMachineClass(self):
        return MachineClass.objects.filter(Machine_ID = self.id);

    def getArrayLabelClass(self):
        data = []
        mc = MachineClass.objects.filter(Machine_ID = self.id)
        for c in mc:
            data.append(c.Name)
        return data

    def getExportFile(self):
        zipfile = os.path.join(self.Directory, "model.zip");
        zipObj = ZipFile(file=zipfile, mode='w')
        zipObj.write(os.path.join(self.Directory, "model.h5"), "model.h5")
        zipObj.write(os.path.join(self.Directory, "model.json"), "model.json")
        zipObj.close()
        return zipfile;

class MachineClass (models.Model):
    Name = models.CharField(max_length=255)
    Machine_ID = models.CharField(max_length=255, default="0")
    ClassEncoding = models.CharField(max_length=255, default="")
    