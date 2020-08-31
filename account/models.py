from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.translation import gettext_lazy as _


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(verbose_name=_("Bio"), max_length=500, blank=True)
    location = models.CharField(verbose_name=_("Location"), max_length=80, blank=True)
    position = models.ForeignKey('Position', on_delete=models.PROTECT, blank=True, null=True)
    mobile_phone = models.CharField(verbose_name=_("Mobile phone"), max_length=50, blank=True)
    internal_phone = models.CharField(verbose_name=_("Internal phone"), max_length=50, blank=True)
    avatar = models.ImageField(upload_to='avatars', default='default_avatar.png')


class Position(models.Model):
    name = models.CharField(verbose_name=_("Position"), max_length=50, blank=True)

    def __str__(self):
        return self.name


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
