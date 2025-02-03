from django.shortcuts import render,redirect,HttpResponse
from events.models import Event 
from events.forms import EventModelForm,CategoryModelForm,CustomRegisterForm,LoginForm,AssignRoleForm,CreateGroupForm
from django.db.models import Q
from django.contrib import messages
from django.utils import timezone
from django.contrib.auth import login,logout
from django.contrib.auth.models import User,Group
from django.contrib.auth.tokens import default_token_generator
from django.db.models import Prefetch
from django.contrib.auth.decorators import user_passes_test, login_required, permission_required

# Create your views here.
def is_admin(user):
    return user.groups.filter(name='Admin').exists()

def is_manager(user):
    return user.groups.filter(name='Manager').exists()

def is_employee(user):
    return user.groups.filter(name='Employee').exists()


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

@user_passes_test(is_admin, login_url='no-permission')
def dashboard(request):
    type = request.GET.get('type')
    upcoming_events_count = Event.get_upcoming_events().count()
    past_events = Event.objects.filter(date__lt=timezone.now()).count()
    all_events = Event.objects.select_related('category').order_by('date')

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
    total_participant = User.objects.count()
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


@user_passes_test(is_admin, login_url='no-permission')
def create_event(request):
    form = EventModelForm()
    if request.method == "POST":
        event_form = EventModelForm(request.POST,request.FILES)
        if event_form.is_valid():
            event_form.save()
            messages.success(request,"Events Created Successfully!!")
        else:
            messages.error(request, "Unable to create participant. Please provide correct information!")
    return render(request,'create_event/create_event.html',{"form":form})

@user_passes_test(is_admin, login_url='no-permission')
def create_category(request):
    form = CategoryModelForm()
    if request.method == "POST":
        cate_form = CategoryModelForm(request.POST)
        if cate_form.is_valid():
            cate_form.save()
            messages.success(request,"Category Created Successfully.Now create Participants")
    return render(request,'create/create_cate.html',{"form":form})


# @user_passes_test(is_admin, login_url='no-permission')
# def create_participant(request):
#     form = ParticipantModelForm()
#     if request.method == "POST":
#         part_form = ParticipantModelForm(request.POST)
#         if part_form.is_valid():
#             part_form.save()
#             messages.success(request,"Participants Created Successfully. Now create Events. Okay!")
#         else:
#             messages.error(request, "Unable to create participant. Please provide unique email")
#     return render(request,'create/create_part.html',{"form":form})


@user_passes_test(is_admin, login_url='no-permission')
def delete_event(request, event_id):
    event = Event.objects.get(id=event_id)
    if request.method == 'POST':
        event.delete()
        messages.success(request, 'Event deleted successfully.')
        return redirect('dashboard')
    return redirect('dashboard')


@user_passes_test(is_admin, login_url='no-permission')
def update_event(request, event_id):
    event = Event.objects.get(id=event_id)
    if request.method == 'POST':
        form = EventModelForm(request.POST, request.FILES, instance=event,)
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


@login_required
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

@user_passes_test(is_admin, login_url='no-permission')
def admin_dashboard(request):
    users = User.objects.prefetch_related(
        Prefetch('groups', queryset=Group.objects.all(), to_attr='all_groups')
    ).all()
    for user in users:
        if user.all_groups:
            user.group_name = user.all_groups[0].name
        else:
            user.group_name = 'No Group Assigned'
    return render(request, 'admin/dashboard.html', {"users": users})

@user_passes_test(is_admin, login_url='no-permission')
def assign_role(request,user_id):
    user = User.objects.get(id=user_id)
    form = AssignRoleForm()

    if request.method == 'POST':
        form = AssignRoleForm(request.POST)
        if form.is_valid():
            role = form.cleaned_data.get('role')
            user.groups.clear()
            user.groups.add(role)
            messages.success(request, f"User {
                             user.username} has been assigned to the {role.name} role")
            return redirect('admin-dashboard')

    return render(request, 'admin/assign_role.html', {"form": form})

@user_passes_test(is_admin, login_url='no-permission')
def create_group(request):
    form = CreateGroupForm()
    if request.method == 'POST':
        form = CreateGroupForm(request.POST)

        if form.is_valid():
            group = form.save()
            messages.success(request, f"Group {
                             group.name} has been created successfully")
            return redirect('create-group')

    return render(request, 'admin/create_group.html', {'form': form})

@user_passes_test(is_admin, login_url='no-permission')
def group_list(request):
    groups = Group.objects.prefetch_related('permissions').all()
    return render(request, 'admin/group_list.html', {'groups': groups})

def no_permission(request):
    return HttpResponse('You have no permission to access this page')