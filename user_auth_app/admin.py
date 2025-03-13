from django.contrib import admin


# Register your models here.
class AuthorAdmin(admin.ModelAdmin):
    fields = ["username", "email", ]
    

# admin.site.register(AuthorAdmin)