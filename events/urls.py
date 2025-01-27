from django.urls import path
from events.views import home_page,dashboard,details,create_event

urlpatterns = [
    path('home-page/', home_page),
    path('dashboard/', dashboard),
    path('details/', details),
    path('create-event/', create_event),
]