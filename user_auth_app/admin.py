from django.contrib import admin
from user_auth_app.models import CustomUser


# Register your models here.
class AuthorAdmin(admin.ModelAdmin):
    fields = ["username", "email", ]
    

admin.site.register(CustomUser)
# admin.site.register(AuthorAdmin)