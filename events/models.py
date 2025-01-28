from django.db import models

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=250)
    description = models.TextField()
    def __str__(self):
        return self.name

class Participant(models.Model):
    name = models.CharField(max_length=250)
    email = models.EmailField(unique=True)
    def __str__(self):
        return self.name

class Event(models.Model):
    name = models.CharField(max_length=250)
    description = models.TextField()
    date = models.DateField()
    time = models.TimeField()
    location = models.CharField(max_length=200)
    category = models.ForeignKey(Category,on_delete=models.CASCADE,default=1)
    participant = models.ManyToManyField(Participant)
    def __str__(self):
        return self.name