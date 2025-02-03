from django.contrib import admin
from events.models import Category,Event
# from django.contrib.auth.models import User

# Register your models here.
admin.site.register(Event)
admin.site.register(Category)
# admin.site.register(User)