from django.urls import path
from . import views

app_name = 'liauth'


urlpatterns = [
    path('login', views.lilogin, name='login'),
    path('logout', views.lilogout, name='logout'),
    path('register', views.register, name='register'),
    path('captcha', views.send_email_captcha, name='email_captcha'),
    path('profile', views.profile_detail, name='profile_detail'),
    path('profile/edit', views.profile_edit, name='profile_edit'),
    path('profile/<int:user_id>', views.profile_detail, name='profile_detail_by_id'),
]