from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

# Create your models here.


class CaptchaModel(models.Model):
    email = models.EmailField(unique=True)
    captcha = models.CharField(max_length=4)
    creat_time = models.DateTimeField(auto_now_add=True)


class Profile(models.Model):
    """用户个人信息模型"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile', verbose_name='用户')
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True, verbose_name='头像')
    bio = models.TextField(max_length=500, blank=True, verbose_name='个人简介')
    website = models.URLField(max_length=200, blank=True, verbose_name='个人主页')
    location = models.CharField(max_length=100, blank=True, verbose_name='所在地')
    birthday = models.DateField(blank=True, null=True, verbose_name='生日')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    def __str__(self):
        return f"{self.user.username}的个人资料"

    class Meta:
        verbose_name = '用户资料'
        verbose_name_plural = verbose_name