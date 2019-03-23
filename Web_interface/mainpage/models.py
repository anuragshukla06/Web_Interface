from django.db import models
import datetime

# Create your models here.
class Entry(models.Model):
    start_date = models.DateTimeField(default=datetime.datetime.now())
    end_date = models.DateTimeField()
    fruit = models.CharField(max_length=200)
    running = models.BooleanField(default=False)
    dataRecord = models.FileField(null=True)

    # def __str__(self):
    #     print(self.fruit + " " + str(self.start_date) + " " + str(self.end_date) +" "+ str(self.running))

class PreSavedData(models.Model):
    fruit = models.CharField(max_length=200)
    temperature = models.IntegerField()
    relative_humidity = models.IntegerField()
    numberOfDays = models.IntegerField()

class CurrentParameters(models.Model):
    fruit = models.CharField(max_length=200)
    temperature =models.IntegerField()
    relative_humidity = models.IntegerField()
    light = models.IntegerField(default=0)
