from django.contrib import admin
from .models import Contacts, Task

# Register your models here.

admin.site.register(Contacts)
admin.site.register(Task)