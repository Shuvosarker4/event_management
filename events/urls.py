from django.urls import path
from events.views import home_page,dashboard,details,create_event

urlpatterns = [
    path('home-page/', home_page,name="home"),
    path('dashboard/', dashboard,name="dashboard"),
    path('details/<int:event_id>/', details,name='event_details'),
    path('create-event/', create_event,name="create-event"),
]