from django.db.models.signals import post_save
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings

from .models import Post
from blogx.models import NewsLetter


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
