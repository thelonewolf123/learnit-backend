from django.shortcuts import render, redirect, reverse
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings

from .models import FreeCourse, FreeLesson, Subscription, Review, Category, Tag


def index(request):
    context = {}
    context['home_nav'] = 'active'
    return render(request, 'learnit/home.html', context=context)


def courses(request):

    context = {}
    courses = FreeCourse.objects.all()
    page_number = request.GET.get('page')
    paginator = Paginator(courses, 5)

    categories = Category.objects.all()

    try:
        page_obj = paginator.get_page(page_number)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)

    context['courses'] = page_obj
    context['page_obj'] = page_obj
    context['categories'] = Category.objects.all()
    context['tags'] = Tag.objects.all()
    context['course_nav'] = 'active'

    if courses.count() > 5:
        context['is_paginated'] = True

    return render(request, 'learnit/course-list.html', context=context)


def course_detail(request, course):

    context = {}
    try:
        context['course'] = FreeCourse.objects.get(slug=course)
        context['categories'] = Category.objects.all()
        context['tags'] = Tag.objects.all()
    except Exception as e:
        print(e)
        raise Http404
    return render(request, 'learnit/single-course.html', context=context)


@login_required
def course_learning(request, course):
    context = {}
    try:
        course_obj = FreeCourse.objects.get(slug=course)
        default_lesson = FreeLesson.objects.filter(course=course_obj).first()
        lesson = request.GET.get('lesson', default_lesson.slug)
    except Exception as e:
        raise Http404

    try:
        user = request.user
        subscription = Subscription.objects.filter(
            user=user).filter(course=course_obj)
        context['lessons'] = FreeLesson.objects.filter(course=course_obj)
        context['lesson'] = FreeLesson.objects.get(slug=lesson)
        context['course'] = course_obj
    except Exception as e:
        print(e)
        raise Http404

    if subscription.count() == 0:
        messages.error(
            request, 'To access this course first you need to enroll it.')
        return redirect('course-detail', course=course.slug)

    return render(request, 'learnit/course-galary.html', context=context)


@login_required
def course_enroll(request, course):

    try:
        course = FreeCourse.objects.get(slug=course)
        user = request.user
        subscription = Subscription.objects.filter(
            user=user).filter(course=course)
    except Exception as e:
        print(e)
        raise Http404

    if subscription.count() == 0:
        Subscription.objects.create(user=user, course=course)
        messages.success(request, 'Your course has been enrolled.')
        return redirect('course-detail', course=course.slug)
    else:
        messages.error(request, 'You already enrolled this course.')
        return redirect('course-detail', course=course.slug)


@login_required
def my_courses(request):
    context = {}
    try:
        user = request.user
        subscription = Subscription.objects.filter(user=user)
        context['categories'] = Category.objects.all()
        context['tags'] = Tag.objects.all()
        for sub in subscription:
            print(sub.course)
        context['courses'] = subscription
    except Exception as e:
        print(e)
        raise Http404

    return render(request, 'learnit/my-courses.html', context=context)


def course_search(request):

    context = {}
    search = request.GET['s']
    try:
        courses = FreeCourse.objects.filter(title__icontains=search)
    except Exception as e:
        print(e)
        raise Http404

    page_number = request.GET.get('page')
    paginator = Paginator(courses, 5)

    categories = Category.objects.all()

    try:
        page_obj = paginator.get_page(page_number)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)

    context['courses'] = page_obj
    context['page_obj'] = page_obj
    context['categories'] = Category.objects.all()
    context['tags'] = Tag.objects.all()
    context['searchx'] = search

    if courses.count() > 5:
        context['is_paginated'] = True

    return render(request, 'learnit/course-list.html', context=context)


def course_category(request):

    context = {}
    category = request.GET['c']
    try:
        cat = Category.objects.get(name=category)
        courses = FreeCourse.objects.filter(category=cat)
    except Exception as e:
        print(e)
        raise Http404

    page_number = request.GET.get('page')
    paginator = Paginator(courses, 5)

    categories = Category.objects.all()

    try:
        page_obj = paginator.get_page(page_number)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)

    context['courses'] = page_obj
    context['page_obj'] = page_obj
    context['categories'] = categories
    context['tags'] = Tag.objects.all()
    context['catx'] = category

    if courses.count() > 5:
        context['is_paginated'] = True

    return render(request, 'learnit/course-list.html', context=context)

# def course_tag(request):
#     context = {}
#     tag = request.GET['t']
#     try:
#         context['courses'] = FreeCourse.objects.filter(tag__icontains=tag)
#         context['categories'] = Category.objects.all()
#         context['tags'] = Tag.objects.all()
#         context['tagx'] = tag
#     except:
#         raise Http404

#     return render(request, 'learnit/course-list.html', context=context)


@login_required
def ask_instructor(request):
    try:
        course = request.POST['course']
        lesson = request.POST['lesson']
        subject = request.POST['subject']
        message = request.POST['question']
        user = request.user.email
        mail_subject = f'[Learning platform] {subject}'
        mail_body = f'User Email: {user}\nCourse: {course}\nLesson: {lesson}\n\n{message}'
        send_mail(mail_subject, mail_body, settings.EMAIL_HOST_USER,
                  settings.ADMIN_EMAIL_ADDRESS)

        messages.success(
            request, 'Your message has ben sent, soon the admin will contact you.')

        return HttpResponseRedirect(reverse('course-learn', args=(course,))+"?lesson="+lesson)

    except Exception as e:
        print(e)
        raise Http404


def profile(request):
    return HttpResponse("Peofile of "+str(request.user.email))
