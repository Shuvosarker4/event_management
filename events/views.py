from django.shortcuts import render
from events.models import Event,Participant
from django.db.models import Q
# Create your views here.
def home_page(request):
    query = request.GET.get('q')
    if query:
        all_events = Event.objects.filter(
            Q(name__icontains=query) |
            Q(location__icontains=query)
        )
        if not all_events.exists():
            return render(request, 'home_page/home_page.html', {"message": "Event not found"})
    else:
        all_events = Event.objects.all()
    context = {"events":all_events,"query": query}
    return render(request,'home_page/home_page.html',context)

def dashboard(request):
    type = request.GET.get('total-event')
    if type == 'total-event':
        all_events = Event.objects.all()
    all_events = Event.objects.all()
    total_event = all_events.count()
    total_participant = Participant.objects.count()
    context = {"total_event":total_event,
               "total_participant":total_participant,
               "all_events":all_events}
    return render(request,'dashboard/dashboard.html',context)

def details(request,event_id):
    event = Event.objects.get(id=event_id)
    print(event.name)
    return render(request,'details/details.html',{"event":event})


def create_event(request):
    return render(request,'create_event/create_event.html')