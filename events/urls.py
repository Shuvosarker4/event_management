from django.urls import path
from events.views import home_page,dashboard,details,create_event,create_category,create_participant,delete_event,update_event,sign_up,sign_in,sign_out,activate_user

urlpatterns = [
    path('home-page/', home_page,name="home"),
    path('dashboard/', dashboard,name="dashboard"),
    path('details/<int:event_id>/', details,name='event_details'),
    path('create-event/', create_event,name="create-event"),
    path('create-category/', create_category,name="create-category"),
    path('create-participant/', create_participant,name="create-participant"),
    path('delete_event/<int:event_id>/', delete_event, name='delete_event'),
    path('update_event/<int:event_id>/', update_event, name='update_event'),
    path('sign_up/',sign_up,name="sign-up"),
    path('sign-in/', sign_in,name='sign-in'),
    path('sign-out/', sign_out,name='sign-out'),
    path('activate/<int:event_id>/<str:token>/',activate_user,name='activate-user'),
]