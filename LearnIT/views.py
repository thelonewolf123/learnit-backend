from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import Http404

from blogx.models import NewsLetter


def about(request):
    context = {}
    context['about_nav'] = 'active'
    return render(request, 'learnit/about-us.html', context=context)


def contact(request):
    context = {}
    context['contact_nav'] = 'active'
    if request.method == 'POST':
        pass

    return render(request, 'learnit/contact-us.html', context=context)
