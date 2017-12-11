from django.contrib import admin
from app01 import models
# Register your models here.

admin.site.register(models.User)
admin.site.register(models.RoomDetail)
admin.site.register(models.Room)



