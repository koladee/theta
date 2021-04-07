from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from datetime import datetime, timezone
import time


class Profile(models.Model):
    id = models.AutoField(primary_key=True, unique=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    rid = models.CharField(max_length=100, blank=False)
    level = models.CharField(max_length=20, blank=False)
    hidden_toggle = models.BooleanField(default=True, blank=True)
    public_toggle = models.BooleanField(default=True, blank=True)
    mod_permission = models.BooleanField(default=False, blank=True)
    bot_pause = models.BooleanField(default=False, blank=True)
    language = models.CharField(max_length=20, default="english")
    access_token = models.CharField(max_length=200, default="", blank=True)
    refresh_token = models.CharField(max_length=200, default="", blank=True)
    reg_date = models.DateTimeField(default=datetime.now, blank=True)

    def __str__(self):
        return self.user.email


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


class Chat(models.Model):
    id = models.AutoField(primary_key=True, unique=True)
    rid = models.CharField(max_length=20, blank=False)
    command = models.TextField(blank=False)
    sender = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='Chat')
    remark = models.TextField(blank=True)
    created_date = models.DateTimeField(default=datetime.now, blank=True)

    def __str__(self):
        return self.command


class Config(models.Model):
    id = models.AutoField(primary_key=True, unique=True)
    key = models.CharField(max_length=100, blank=False)
    user = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='Config')
    content = models.TextField(blank=False)
    permission = models.CharField(max_length=100, blank=True)
    minlvl = models.IntegerField(default=int(0))
    maxlvl = models.IntegerField(default=int(100))
    modified_date = models.DateTimeField(default=datetime.now, blank=True)
    created_date = models.DateTimeField(default=datetime.now, blank=True)

    def __str__(self):
        return self.key+' <'+self.user.user.email+'>'


class Timer(models.Model):
    id = models.AutoField(primary_key=True, unique=True)
    key = models.CharField(max_length=100, blank=False)
    user = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='Timer')
    content = models.TextField(blank=False)
    minutes = models.CharField(max_length=100, blank=False)
    fire_time = models.IntegerField(default=0, blank=False)
    status = models.BooleanField(default=True)
    fired = models.BooleanField(default=False)
    viewers = models.TextField(default="//", blank=True)
    created_date = models.DateTimeField(default=datetime.now, blank=True)

    def __str__(self):
        return self.key+' <'+self.minutes+' minute(s)>'


class List(models.Model):
    id = models.AutoField(primary_key=True, unique=True)
    key = models.CharField(max_length=100, blank=False)
    user = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='List')
    content = models.TextField(blank=False)
    created_date = models.DateTimeField(default=datetime.now, blank=True)

    def __str__(self):
        return self.key+' <'+self.user.user.username+'>'


class Reward(models.Model):
    id = models.AutoField(primary_key=True, unique=True)
    level = models.IntegerField(default=0, blank=False)
    reward_type = models.CharField(max_length=100, blank=False, default="")
    reward = models.TextField(blank=False)
    user = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='Reward')
    created_date = models.DateTimeField(default=datetime.now, blank=False)

    def __str__(self):
        return str(self.level)+' <'+self.user.user.username+'>'

