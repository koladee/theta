from django.contrib import admin
from .models import Profile, Chat, Config, Timer, List

# Register your models here.
admin.site.register(Profile)
admin.site.register(Chat)
admin.site.register(Config)
admin.site.register(Timer)
admin.site.register(List)
