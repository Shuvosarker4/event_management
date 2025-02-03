from django.shortcuts import render,redirect,HttpResponse
from events.models import Event,Participant 
from events.forms import EventModelForm,CategoryModelForm,ParticipantModelForm,CustomRegisterForm,LoginForm
from django.db.models import Q
from django.contrib import messages
from django.utils import timezone
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator

# Create your views here.
def home_page(request):
    query = request.GET.get('q','')
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
    type = request.GET.get('type')
    upcoming_events_count = Event.get_upcoming_events().count()
    past_events = Event.objects.filter(date__lt=timezone.now()).count()
    all_events = Event.objects.select_related('category').prefetch_related('participant').order_by('date')

    if type == 'total-event':
        print(type)
        all_events = all_events
    elif type == 'upcoming':
        print(type)
        all_events = all_events.filter(date__gte=timezone.now().date())
    elif type == 'past-event':
        print(type)
        all_events = all_events.filter(date__lt=timezone.now().date())

    total_event = all_events.count()
    total_participant = Participant.objects.count()
    context = {"total_event":total_event,
               "total_participant":total_participant,
               "all_events":all_events,
               "upcoming_events_count":upcoming_events_count,
               "past_events":past_events
               }
    return render(request,'dashboard/dashboard.html',context)

def details(request,event_id):
    event = Event.objects.get(id=event_id)
    print(event.name)
    return render(request,'details/details.html',{"event":event})


def create_event(request):
    form = EventModelForm()
    if request.method == "POST":
        event_form = EventModelForm(request.POST)
        if event_form.is_valid():
            event_form.save()
            messages.success(request,"Events Created Successfully!!")
        else:
            messages.error(request, "Unable to create participant. Please provide correct information!")
    return render(request,'create_event/create_event.html',{"form":form})

def create_category(request):
    form = CategoryModelForm()
    if request.method == "POST":
        cate_form = CategoryModelForm(request.POST)
        if cate_form.is_valid():
            cate_form.save()
            messages.success(request,"Category Created Successfully.Now create Participants")
    return render(request,'create/create_cate.html',{"form":form})

def create_participant(request):
    form = ParticipantModelForm()
    if request.method == "POST":
        part_form = ParticipantModelForm(request.POST)
        if part_form.is_valid():
            part_form.save()
            messages.success(request,"Participants Created Successfully. Now create Events. Okay!")
        else:
            messages.error(request, "Unable to create participant. Please provide unique email")
    return render(request,'create/create_part.html',{"form":form})

def delete_event(request, event_id):
    event = Event.objects.get(id=event_id)
    if request.method == 'POST':
        event.delete()
        messages.success(request, 'Event deleted successfully.')
        return redirect('dashboard')
    return redirect('dashboard')

def update_event(request, event_id):
    event = Event.objects.get(id=event_id)
    if request.method == 'POST':
        form = EventModelForm(request.POST, instance=event)
        if form.is_valid():
            form.save()
            messages.success(request, 'Event updated successfully.')
            return redirect('dashboard')
    else:
        form = EventModelForm(instance=event)
    return render(request, 'create_event/create_event.html', {'form': form})

def sign_up(request):
    form =CustomRegisterForm()
    if request.method == "POST":
        form = CustomRegisterForm(request.POST)
        if form.is_valid():
            user=form.save(commit=False)
            user.set_password(form.cleaned_data.get('password'))
            user.is_active = False
            user.save()
            messages.success(request,"A confirmation mail has been send on your mail.please check!")
            return redirect('sign-in')
        else:
            print('Form is not valid')
    return render(request,'registration/register.html',{"form":form})

def sign_in(request):
    form = LoginForm()
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request,user)
            return redirect('home')
    return render(request,'registration/login.html',{'form':form})


def sign_out(request):
    if request.method == 'POST':
        logout(request)
        return redirect('home')
    
def activate_user(request,event_id,token): 
    try:
        user = User.objects.get(id=event_id)
        if default_token_generator.check_token(user,token):
            user.is_active =True
            user.save()
            messages.success(request,'You are verified,please login now!')
            return redirect('sign-in')
        else:
            return HttpResponse('Invalid Id')
    except User.DoesNotExist:
        return HttpResponse('User Not Found')