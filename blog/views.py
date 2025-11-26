from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.db.models import Q
from django.http.response import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views.decorators.http import require_GET, require_POST, require_http_methods
from django.views.generic import ListView

from .forms import BlogCommentForm, PubBlogForm
from .models import Blog, BlogCategory, BlogComment


def _paginate_queryset(request, queryset, per_page=10):
    """内部工具：根据请求分页并返回 (page_obj, object_list)。"""
    paginator = Paginator(queryset, per_page)
    if paginator.count == 0:
        return None, list(queryset)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)
    return page_obj, page_obj.object_list


def index(request):
    """博客首页：展示最新博客列表"""
    blog_qs = Blog.objects.select_related('author', 'author__profile', 'category').prefetch_related('comments')
    page_obj, blogs = _paginate_queryset(request, blog_qs)
    return render(request, 'index.html', context={"blogs": blogs, "page_obj": page_obj})


def blog_detail(request, blog_id):
    """博客详情页"""
    blog = get_object_or_404(
        Blog.objects.select_related('author', 'category').prefetch_related('comments__author__profile'),
        pk=blog_id
    )
    return render(request, 'blog_detail.html', context={'blog': blog})


@require_http_methods(['GET', 'POST'])
@login_required
def pub_blog(request):
    """发布博客，支持AJAX提交"""
    if request.method == 'GET':
        categories = BlogCategory.objects.all().only('id', 'name')
        return render(request, 'pub_blog.html', context={"categories": categories})

    form = PubBlogForm(request.POST)
    if form.is_valid():
        blog = Blog.objects.create(
            title=form.cleaned_data['title'],
            content=form.cleaned_data['content'],
            category_id=form.cleaned_data['category'],
            author=request.user
        )
        return JsonResponse({"code": 200, "message": "博客发布成功！", "data": {"blog_id": blog.id}})

    return JsonResponse({"code": 400, "message": "参数错误！", "errors": form.errors}, status=400)


@require_POST
@login_required
def pub_comment(request):
    """发布评论"""
    blog_id = request.POST.get('blog_id')
    blog = get_object_or_404(Blog, pk=blog_id)
    form = BlogCommentForm(request.POST)
    if not form.is_valid():
        messages.error(request, '评论提交失败：{}'.format(form.errors.get('content', ['内容不合法'])[0]))
        return redirect(reverse("blog:blog_detail", kwargs={'blog_id': blog_id}))

    BlogComment.objects.create(content=form.cleaned_data['content'], blog=blog, author=request.user)
    messages.success(request, '评论发布成功！')
    return redirect(reverse("blog:blog_detail", kwargs={'blog_id': blog_id}))


@require_GET
def search(request):
    """根据关键字搜索博客"""
    q = request.GET.get('q', '').strip()
    blogs = Blog.objects.select_related('author', 'author__profile', 'category').filter(
        Q(title__icontains=q) | Q(content__icontains=q)
    ) if q else Blog.objects.none()
    page_obj, paginated_blogs = _paginate_queryset(request, blogs)
    return render(
        request,
        'index.html',
        context={"blogs": paginated_blogs, "page_obj": page_obj, "search_query": q}
    )


class MyBlogListView(LoginRequiredMixin, ListView):
    """展示当前登录用户的博客列表"""

    model = Blog
    template_name = 'my_blogs.html'
    context_object_name = 'blogs'
    paginate_by = 10

    def get_queryset(self):
        return (
            super()
            .get_queryset()
            .select_related('author', 'author__profile', 'category')
            .prefetch_related('comments')
            .filter(author=self.request.user)
        )


@require_POST
@login_required
def delete_blog(request, blog_id):
    """删除当前用户的博客，未授权则提示"""
    blog = get_object_or_404(Blog, pk=blog_id)
    if blog.author != request.user:
        messages.error(request, '只能删除自己的博客。')
        return redirect(reverse('blog:my_blogs'))

    blog.delete()
    messages.success(request, '博客已删除。')
    return redirect(reverse('blog:my_blogs'))

