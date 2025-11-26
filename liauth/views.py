from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.http.response import JsonResponse
import string
import random
from django.core.mail import send_mail
from .models import CaptchaModel, Profile
from django.views.decorators.http import require_http_methods
from .forms import RegisterForm, LoginForm, ProfileForm
from django.contrib.auth import get_user_model, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

User = get_user_model()

# Create your views here.
@require_http_methods(['GET', 'POST'])
def lilogin(request):
    if request.method == 'GET':
        return render(request, 'login.html')
    else:
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            remember_me = form.cleaned_data['remember_me']
            user = User.objects.filter(email=email).first()
            if user and user.check_password(password):
                # 登录
                login(request, user)
                user.is_authenticated
                # 判断是否需要记住我
                if not remember_me:
                    # 如果未点击记住我，设置过期时间为0，即浏览器关闭后过期
                    request.session.set_expiry(0)
                # 如果点击了，即为2周默认过期时间
                return redirect('/')
            else:
                # 登录失败：返回登录页并给出用户友好的提示
                return redirect(reverse('liauth:login'))


def lilogout(request):
    logout(request)
    return redirect('/')


@require_http_methods(['GET', 'POST'])
def register(request):
    if request.method == 'GET':
        return render(request, 'register.html')
    else:
        form = RegisterForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            User.objects.create_user(email=email, username=username, password=password)
            return redirect(reverse('liauth:login'))
        else:
            # 表单校验失败：可以在此处增加 messages 提示，当前先简单重定向
            return redirect(reverse('liauth:register'))
            # return render(request, 'register.html', context={"form": form})


def send_email_captcha(request):
    # ?email=xxx
    email = request.GET.get('email')
    if not email:
        return JsonResponse({"code": 400, "message": '必须传递邮箱！'})
    # 生成验证码（随机4位阿拉伯数字）
    captcha = "".join(random.sample(string.digits, 4))
    # 存储到数据库中
    CaptchaModel.objects.update_or_create(email=email, defaults={ 'captcha': captcha })
    send_mail("博客注册验证", message=f"您的注册验证码是: {captcha}", recipient_list=[email], from_email=None)
    return JsonResponse({"code": 200, "message": "邮箱验证码发送成功！ "})


@login_required
def profile_detail(request, user_id=None):
    """展示个人信息页面"""
    if user_id:
        # 查看其他用户的个人信息
        user = get_object_or_404(User, pk=user_id)
    else:
        # 查看自己的个人信息
        user = request.user
    
    # 获取或创建Profile（如果不存在则自动创建）
    profile, created = Profile.objects.get_or_create(user=user)
    
    return render(request, 'profile_detail.html', {
        'profile_user': user,
        'profile': profile,
        'is_own_profile': user == request.user
    })


@require_http_methods(['GET', 'POST'])
@login_required
def profile_edit(request):
    """编辑个人信息页面"""
    profile, created = Profile.objects.get_or_create(user=request.user)
    
    if request.method == 'GET':
        form = ProfileForm(instance=profile)
        return render(request, 'profile_edit.html', {'form': form, 'profile': profile})
    else:
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect(reverse('liauth:profile_detail'))
        else:
            return render(request, 'profile_edit.html', {'form': form, 'profile': profile})