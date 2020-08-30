import uuid
import os

from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.shortcuts import reverse
from datetime import datetime
from django.dispatch import receiver

from django.db.models.signals import post_save
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings


class Category(models.Model):
    name = models.CharField(max_length=200, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Categories"


class Tag(models.Model):
    name = models.CharField(max_length=200, unique=True)

    def __str__(self):
        return self.name


class Author(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='blog_posts')
    name = models.CharField(max_length=200, unique=True)
    discription = models.TextField(max_length=600)
    profile = models.ImageField(upload_to='profile/')

    def __str__(self):
        return self.name


class Post(models.Model):
    title = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True)
    title_img = models.ImageField(null=False, upload_to='blog/images')
    title_dics = models.TextField(max_length=600)
    author = models.ForeignKey(
        Author, on_delete=models.CASCADE, related_name='blog_posts')
    category = models.ForeignKey(Category, on_delete=models.DO_NOTHING)
    updated_on = models.DateTimeField(auto_now=True)
    tags = models.CharField(max_length=200, unique=True)
    content = models.TextField(null=False, max_length=20000)
    created_day = models.CharField(null=False, max_length=4)
    created_month = models.CharField(null=False, max_length=40)
    created_year = models.CharField(null=False, max_length=5)

    class Meta:
        ordering = ['-id']

    def __str__(self):
        return self.title

    def _get_unique_slug(self):
        slug = slugify(self.title)
        unique_slug = slug
        num = 1
        while Post.objects.filter(slug=unique_slug).exists():
            unique_slug = '{}-{}'.format(slug, num)
            num += 1
        return unique_slug

    def _get_month(self, month):
        monthDict = {1: 'Jan', 2: 'Feb', 3: 'Mar', 4: 'Apr', 5: 'May', 6: 'Jun',
                     7: 'Jul', 8: 'Aug', 9: 'Sep', 10: 'Oct', 11: 'Nov', 12: 'Dec'}

        return monthDict[int(month)]

    def get_absolute_url(self):

        return reverse('single_blog', args=(self.slug,))

    def seo_discription(self):

        if len(self.title_dics) > 155:

            return self.title_dics[:150] + '...'

        return self.title_dics

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self._get_unique_slug()
        today = datetime.today()
        self.created_day = str(today.day)
        self.created_month = self._get_month(str(today.month))
        self.created_year = str(today.year)

        super().save(*args, **kwargs)


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    name = models.CharField(null=False, blank=False, max_length=30)
    message = models.TextField(null=False, max_length=700)
    created_day = models.CharField(null=False, max_length=4)
    created_month = models.CharField(null=False, max_length=40)
    created_year = models.CharField(null=False, max_length=5)

    def _get_month(self, month):
        monthDict = {1: 'Jan', 2: 'Feb', 3: 'Mar', 4: 'Apr', 5: 'May', 6: 'Jun',
                     7: 'Jul', 8: 'Aug', 9: 'Sep', 10: 'Oct', 11: 'Nov', 12: 'Dec'}

        return monthDict[int(month)]

    def save(self, *args, **kwargs):
        today = datetime.today()
        self.created_day = str(today.day)
        self.created_month = self._get_month(str(today.month))
        self.created_year = str(today.year)

        super().save(*args, **kwargs)

    def __str__(self):
        return self.message


class NewsLetter(models.Model):

    email = models.EmailField(null=False, blank=False, max_length=200)
    uid = models.CharField(max_length=100, null=False, unique=True)
    created = models.DateTimeField(auto_now_add=True)

    def get_absolute_url(self):

        return reverse('unsubscribe', args=(self.uuid,))

    def __str__(self):
        return self.email

    def save(self, *args, **kwargs):
        self.uid = str(uuid.uuid4())
        super().save(*args, **kwargs)

@receiver(post_save, sender=Post)
def submission_delete(sender, instance, **kwargs):

    news_letters = NewsLetter.objects.all()

    context = {}
    context['title_img'] = instance.title_img
    context['category'] = instance.category.name
    context['discription'] = instance.title_dics
    context['url'] = instance.get_absolute_url()

    subject, from_email = '[CyberKrypts.com] Check out our new article', settings.EMAIL_HOST_USER

    to = []

    for news_letter in news_letters:

        to = news_letter.email
        context['unsubscribe_url'] = news_letter.get_absolute_url()
        text_content = ''
        html_content = render_to_string(
            'blogx/email-news-letter.txt', context=context)
        msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
        msg.attach_alternative(html_content, "text/html")
        msg.send()
