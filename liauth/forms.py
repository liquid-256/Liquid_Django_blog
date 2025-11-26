from django import forms
from django.contrib.auth import get_user_model
from .models import CaptchaModel, Profile


User = get_user_model()


class ProfileForm(forms.ModelForm):
    """个人信息编辑表单"""
    class Meta:
        model = Profile
        fields = ['avatar', 'bio', 'website', 'location', 'birthday']
        widgets = {
            'avatar': forms.FileInput(attrs={'class': 'form-control'}),
            'bio': forms.Textarea(attrs={'class': 'form-control', 'rows': 5, 'placeholder': '介绍一下自己吧...'}),
            'website': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'https://example.com'}),
            'location': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '例如：北京'}),
            'birthday': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }
        labels = {
            'avatar': '头像',
            'bio': '个人简介',
            'website': '个人主页',
            'location': '所在地',
            'birthday': '生日',
        }

    def clean_website(self):
        website = self.cleaned_data.get('website')
        if website and not website.startswith(('http://', 'https://')):
            website = 'https://' + website
        return website


class RegisterForm(forms.Form):
    username = forms.CharField(max_length=20, min_length=2, error_messages={
        'required': '请传入用户名',
        "max_length": '用户名长度在2~20之间',
        "min_length": '用户名长度在2~20之间',
    })
    email = forms.EmailField(error_messages={"required": '请传入邮箱', 'invalid': '请传入一个正确的邮箱！'})
    captcha = forms.CharField(max_length=4, min_length=4)
    password = forms.CharField(max_length=20, min_length=6)

    def clean_email(self):
        email = self.cleaned_data.get('email')
        user_exists = User.objects.filter(email=email).exists()
        if user_exists:
            raise forms.ValidationError('此邮箱已被注册！')
        return email

    def clean_captcha(self):
        captcha = self.cleaned_data.get('captcha')
        email = self.cleaned_data.get('email')

        captcha_model = CaptchaModel.objects.filter(email=email, captcha=captcha).first()
        if not captcha_model:
            raise forms.ValidationError("验证码和邮箱不匹配！")
        captcha_model.delete()
        return captcha


class LoginForm(forms.Form):
    email = forms.EmailField(error_messages={"required": '请传入邮箱', 'invalid': '请传入一个正确的邮箱！'})
    password = forms.CharField(max_length=20, min_length=6)
    remember_me = forms.IntegerField(required=False)