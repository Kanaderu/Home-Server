from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.translation import gettext as _


class Profile(models.Model):
    GENDER_TYPE = (
        ('F', 'Female'),
        ('M', 'Male'),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    city = models.CharField(max_length=30, blank=True)
    state = models.CharField(max_length=2, blank=True)
    gender = models.CharField(max_length=1, choices=GENDER_TYPE, blank=True)
    is_active = models.BooleanField(_('active'), default=True)

    def __str__(self):
        return self.user.first_name + ' ' + self.user.last_name


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
