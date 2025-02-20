from django.urls import path
from django.contrib.auth.views import PasswordChangeDoneView
from events.views import home_page,dashboard,details,create_event,create_category,delete_event,update_event,sign_up,sign_in,sign_out,activate_user,admin_dashboard,assign_role,create_group,group_list,no_permission,rsvp_event,CreateEvent,CreateCategory,UpdateEvent,DeleteEvent,SignIn,Profile,ChangePassword,CustomPasswordResetView,CustomPasswordResetConfirmView

urlpatterns = [
    path('home-page/', home_page,name="home"),
    path('dashboard/', dashboard,name="dashboard"),
    path('profile/', Profile,name="profile"),
    path('details/<int:event_id>/', details,name='event_details'),
    # path('create-event/', create_event,name="create-event"),
    path('create-event/', CreateEvent.as_view(),name="create-event"),
    path('create-category/', CreateCategory.as_view(),name="create-category"),
    # path('create-category/', create_category,name="create-category"),
    path('delete_event/<int:event_id>/', DeleteEvent.as_view(), name='delete_event'),
    # path('delete_event/<int:event_id>/', delete_event, name='delete_event'),
    # path('update_event/<int:event_id>/', update_event, name='update_event'),
    path('update_event/<int:event_id>/', UpdateEvent.as_view(), name='update_event'),


    path('sign_up/',sign_up,name="sign-up"),
    path('sign-in/', SignIn.as_view(),name='sign-in'),
    # path('sign-in/', sign_in,name='sign-in'),
    path('sign-out/', sign_out,name='sign-out'),
    path('activate/<int:event_id>/<str:token>/',activate_user,name='activate-user'),

    path('admin/dashboard/', admin_dashboard, name='admin-dashboard'),
    path('admin/<int:user_id>/assign-role/', assign_role, name='assign-role'),
    path('admin/create-group/', create_group, name='create-group'),
    path('admin/group-list/', group_list, name='group-list'),

    path('no-permission/', no_permission, name='no-permission'),
    path('rsvp-event/<int:event_id>/',rsvp_event, name="rsvp-event"),


    path('password-change/',ChangePassword.as_view(),name="password-change"),
    path('password-change/done/',PasswordChangeDoneView.as_view(template_name="profiles/done.html"),name="password_change_done"),
    path('password-reset/', CustomPasswordResetView.as_view(), name='password_reset'),
    path('password-reset/confirm/<uidb64>/<token>/',CustomPasswordResetConfirmView.as_view(), name='password_reset_confirm')
]