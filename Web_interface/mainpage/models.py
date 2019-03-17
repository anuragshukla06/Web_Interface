from django.db import models

# Create your models here.
class Entry(models.Model):
    start_date = models.DateTimeField(auto_now_add=True);
    end_date = models.DateTimeField(auto_now=False, blank=True);
    fruit = models.CharField(max_length=200);
    running = models.BooleanField(default=False);

    def __str__(self):
        print(self.fruit + " " + str(self.start_date) + " " + str(self.end_date) +" "+ str(self.running))

class PreSavedData(models.Model):
    fruit = models.CharField(max_length=200);
    temperature = models.IntegerField();
    relative_humidity = models.IntegerField();
    numberOfDays = models.IntegerField();