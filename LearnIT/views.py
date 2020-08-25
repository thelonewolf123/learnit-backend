from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import Http404
from django.core.mail import send_mail
from django.conf import settings

from blogx.models import NewsLetter


def about(request):
    context = {}
    context['about_nav'] = 'active'
    return render(request, 'learnit/about-us.html', context=context)


def contact(request):
    context = {}
    context['contact_nav'] = 'active'
    if request.method == 'POST':

        try:
            name = request.POST.get('name')
            email = request.POST.get('email')
            phone_num = request.POST.get('phone')
            message = request.POST.get('message')

            subject = f'[CyberKrypts] Mail from {name}'
            body = f'Email: {email}\n\nPhone: {phone_num}\n\n\n{message}'

            send_mail(subject, body, settings.EMAIL_HOST_USER,
                    settings.ADMIN_EMAIL_ADDRESS)

            messages.success(
                request, "Thank you!!! \nYour message has been sent, soon we'll contact you.")

        except Exception as e:
            print(e)
            messages.error(request,'Something went wrong, Try again.')

        return redirect('index')

    return render(request, 'learnit/contact-us.html', context=context)
