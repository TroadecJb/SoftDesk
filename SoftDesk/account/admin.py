from django.contrib import admin
from account.models import CustomUser


class CustomUserAdmin(admin.ModelAdmin):
    list_display = ("id", "__str__")


admin.site.register(CustomUser, CustomUserAdmin)
