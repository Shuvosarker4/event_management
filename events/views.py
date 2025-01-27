from django.shortcuts import render
# Create your views here.
def home_page(request):
    return render(request,'home_page/home_page.html')

def dashboard(request):
    return render(request,'dashboard/dashboard.html')

def details(request):
    return render(request,'details/details.html')


def create_event(request):
    return render(request,'create_event/create_event.html')