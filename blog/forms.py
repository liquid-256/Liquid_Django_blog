from django import forms
from django.core.exceptions import ValidationError

import bleach

from .models import BlogCategory


class PubBlogForm(forms.Form):
    """发布博客的表单，负责基础字段及富文本清洗。"""

    title = forms.CharField(
        max_length=200,
        min_length=2,
        strip=True,
        error_messages={
            'required': '标题不能为空',
            'max_length': '标题不能超过200个字符',
            'min_length': '标题至少需要2个字符',
        },
    )
    content = forms.CharField(
        min_length=10,
        widget=forms.Textarea,
        error_messages={
            'required': '内容不能为空',
            'min_length': '内容至少需要10个字符',
        },
    )
    category = forms.IntegerField(
        min_value=1,
        error_messages={
            'required': '分类不能为空',
            'invalid': '分类格式不正确',
            'min_value': '分类ID不正确',
        },
    )

    ALLOWED_TAGS = [
        'p', 'br', 'strong', 'em', 'ul', 'ol', 'li',
        'blockquote', 'code', 'pre', 'span', 'a', 'img', 'h1',
        'h2', 'h3', 'h4', 'h5', 'h6'
    ]
    ALLOWED_ATTRIBUTES = {
        '*': ['class'],
        'a': ['href', 'title', 'rel', 'target'],
        'img': ['src', 'alt', 'title']
    }

    def clean_title(self):
        title = self.cleaned_data['title'].strip()
        if not title:
            raise ValidationError('标题不能为空白字符')
        return title

    def clean_content(self):
        raw_content = self.cleaned_data.get('content', '').strip()
        if not raw_content:
            raise ValidationError('内容不能为空白字符')
        cleaned = bleach.clean(
            raw_content,
            tags=self.ALLOWED_TAGS,
            attributes=self.ALLOWED_ATTRIBUTES,
            strip=True
        )
        return cleaned

    def clean_category(self):
        category_id = self.cleaned_data['category']
        if not BlogCategory.objects.filter(id=category_id).exists():
            raise ValidationError('选择的分类不存在')
        return category_id


class BlogCommentForm(forms.Form):
    """发表评论的表单。"""

    content = forms.CharField(
        min_length=2,
        max_length=500,
        strip=True,
        widget=forms.Textarea,
        error_messages={
            'required': '评论内容不能为空',
            'min_length': '评论至少为2个字符',
            'max_length': '评论不能超过500个字符',
        },
    )

    def clean_content(self):
        content = self.cleaned_data['content'].strip()
        if not content:
            raise ValidationError('评论内容不能为空白字符')
        return content