from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from .forms import BlogCommentForm, PubBlogForm
from .models import Blog, BlogCategory, BlogComment


User = get_user_model()


class BlogModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='tester', email='tester@example.com', password='password123')
        self.category = BlogCategory.objects.create(name='Test Category')
        self.blog = Blog.objects.create(title='Test Blog', content='Test Content', category=self.category, author=self.user)
        self.comment = BlogComment.objects.create(blog=self.blog, author=self.user, content='Nice article')

    def test_blog_str(self):
        self.assertEqual(str(self.blog), 'Test Blog')

    def test_blog_comment_str(self):
        self.assertEqual(str(self.comment), 'Nice article')


class BlogViewTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='tester', email='tester@example.com', password='password123')
        self.category = BlogCategory.objects.create(name='Test Category')
        self.blog = Blog.objects.create(title='Test Blog', content='Test Content', category=self.category, author=self.user)

    def test_index_view(self):
        response = self.client.get(reverse('blog:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.blog.title)

    def test_blog_detail_view(self):
        response = self.client.get(reverse('blog:blog_detail', kwargs={'blog_id': self.blog.id}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.blog.title)

    def test_delete_blog_permission(self):
        other_user = User.objects.create_user(username='other', email='other@example.com', password='password123')
        self.client.login(username='other', password='password123')
        response = self.client.post(reverse('blog:delete_blog', kwargs={'blog_id': self.blog.id}))
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Blog.objects.filter(pk=self.blog.id).exists())

        self.client.logout()
        self.client.login(username='tester', password='password123')
        response = self.client.post(reverse('blog:delete_blog', kwargs={'blog_id': self.blog.id}))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Blog.objects.filter(pk=self.blog.id).exists())


class BlogFormTests(TestCase):
    def setUp(self):
        self.category = BlogCategory.objects.create(name='Category')

    def test_pub_blog_form_valid(self):
        form = PubBlogForm(data={'title': 'Valid title', 'content': '<p>valid content 1234567890</p>', 'category': self.category.id})
        self.assertTrue(form.is_valid())

    def test_pub_blog_form_invalid_category(self):
        form = PubBlogForm(data={'title': 'Valid title', 'content': '<p>content</p>' * 5, 'category': 999})
        self.assertFalse(form.is_valid())

    def test_comment_form_validation(self):
        form = BlogCommentForm(data={'content': 'Nice!'})
        self.assertTrue(form.is_valid())
        invalid_form = BlogCommentForm(data={'content': ' '})
        self.assertFalse(invalid_form.is_valid())
