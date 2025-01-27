from django.shortcuts import render
from events.models import Event
# Create your views here.
def home_page(request):
    all_events = Event.objects.all()
    context = {"events":all_events}
    return render(request,'home_page/home_page.html',context)

def dashboard(request):
    return render(request,'dashboard/dashboard.html')

def details(request):
    return render(request,'details/details.html')


def create_event(request):
    return render(request,'create_event/create_event.html')