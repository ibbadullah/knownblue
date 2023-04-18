from django.contrib import admin
from .models import NotificationModel
from usersection.models import SignUpModel


# Register your models here.
admin.site.register(SignUpModel)
admin.site.register(NotificationModel)
