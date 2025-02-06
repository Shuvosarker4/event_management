from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=250)
    description = models.TextField()
    def __str__(self):
        return self.name

class Event(models.Model):
    name = models.CharField(max_length=250)
    description = models.TextField()
    date = models.DateField()
    time = models.TimeField()
    location = models.CharField(max_length=200)
    category = models.ForeignKey(Category,on_delete=models.CASCADE,default=1)
    participant = models.ManyToManyField(User,related_name='rsvp_event', blank=True)
    asset = models.ImageField(upload_to='events_asset',blank=True,null=True,default='events_asset/default.jpg')
    def __str__(self):
        return self.name
    
    @staticmethod
    def get_upcoming_events():
        return Event.objects.filter(date__gte=timezone.now().date())
 