from django.contrib import admin
from .models import Profile, CaptchaModel


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'location', 'birthday', 'created_at']
    list_filter = ['created_at', 'updated_at']
    search_fields = ['user__username', 'user__email', 'location', 'bio']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(CaptchaModel)
class CaptchaModelAdmin(admin.ModelAdmin):
    list_display = ['email', 'captcha', 'creat_time']
    list_filter = ['creat_time']
    search_fields = ['email']
