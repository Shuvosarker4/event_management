from django.dispatch import receiver
from django.db.models.signals import post_save,m2m_changed
from django.contrib.auth.models import User,Group
from django.contrib.auth.tokens import default_token_generator
from django.conf import settings
from django.core.mail import send_mail
from events.models import Event

# send activation email to user
@receiver(post_save,sender=User)
def send_activation_email(sender,instance,created,**kwargs):
    if created:
        token =default_token_generator.make_token(instance)
        activate_url =f"{settings.FRONTEND_URL}/events/activate/{instance.id}/{token}"

        subject = 'Activate Your Account!'
        message = f"Hi {instance.username}.\n\n Please activate your account by clicking the link below:\n{activate_url}\n\n Thank You!"
        recipient_list = [instance.email]
        try:
            send_mail(subject,message,settings.EMAIL_HOST_USER,recipient_list)
        except Exception as e:
            print(f"Failed to send email to {instance.email}:{str(e)}")

@receiver(post_save, sender=User)
def assign_role(sender, instance, created, **kwargs):
    if created:
        user_group, created = Group.objects.get_or_create(name='User')
        instance.groups.add(user_group)
        instance.save()


@receiver(m2m_changed, sender=Event.participant.through)
def send_rsvp_confirmation_email(sender, instance, action, pk_set, **kwargs):
    if action == "post_add":
        for user_id in pk_set:
            user = User.objects.get(pk=user_id)

            subject=f"RSVP Confirmation: {instance.name}"
            message=f"Hello {user.first_name},\n\n"f"You have successfully RSVP'd for the event '{instance.name}'.\n\n"
            recipient_list = [user.email]
            try:
                send_mail(subject,message,settings.EMAIL_HOST_USER,recipient_list)
            except Exception as e:
                print(f"Failed to send email to {instance.email}:{str(e)}")
            