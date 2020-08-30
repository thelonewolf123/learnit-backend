from django.shortcuts import render, redirect, reverse
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings

from .models import Course, Lesson, Subscription, Review, Category, Tag, Payment

import razorpay
client = razorpay.Client(auth=(settings.ROZER_KEY_ID, settings.ROZER_SECRET_KEY))


def index(request):
    courses = Course.objects.all().order_by('-id')
    context = {}
    context['home_nav'] = 'active'
    context['courses'] = courses[0:3]
    return render(request, 'learnit/home.html', context=context)


def courses(request):

    context = {}
    courses = Course.objects.all()
    page_number = request.GET.get('page')
    paginator = Paginator(courses, 5)

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
        context['course'] = Course.objects.get(slug=course)
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
        course_obj = Course.objects.get(slug=course)
        default_lesson = Lesson.objects.filter(course=course_obj).first()
        lesson = request.GET.get('lesson', default_lesson.slug)
    except Exception as e:
        raise Http404

    try:
        user = request.user
        subscription = Subscription.objects.filter(
            user=user).filter(course=course_obj)
        context['lessons'] = Lesson.objects.filter(course=course_obj)
        context['lesson'] = Lesson.objects.get(slug=lesson)
        context['course'] = course_obj
        context['lessonz'] = Lesson.objects.get(slug=lesson)
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
    context = {}

    try:
        course = Course.objects.get(slug=course)
        user = request.user
        subscription = Subscription.objects.filter(
            user=user).filter(course=course)
        
    except Exception as e:
        print(e)
        raise Http404

    if subscription.count() == 0:

        if course.course_type == "free":

            Subscription.objects.create(user=user, course=course)
            messages.success(request, 'Your course has been enrolled.')
            return redirect('my-courses')

        else:

            order_amount = course.price

            order_currency = 'INR'
            order_receipt = 'cyberkeypts_course_order_id'
            notes = {
                'Course': course.title,
                'course-slug': course.slug,
                'user': user.email }

            response = client.order.create(dict(amount=order_amount*100, currency=order_currency, receipt=order_receipt, notes=notes, payment_capture='0'))
            order_id = response['id']
            order_status = response['status']

            if order_status=='created':
                context['product_id'] = course.title
                context['rozer_pay_key'] = settings.ROZER_KEY_ID
                context['price'] = order_amount
                context['email'] = user.email

                # data that'll be send to the razorpay for
                context['order_id'] = order_id
                return render(request, 'learnit/confirm_order.html', context)

            else:
                messages.error(request, 'Something went wrong, try again.')
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
        courses = Course.objects.filter(title__icontains=search)
    except Exception as e:
        print(e)
        raise Http404

    page_number = request.GET.get('page')
    paginator = Paginator(courses, 5)

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

    context['searchx_count'] = courses.count()

    if courses.count() > 5:
        context['is_paginated'] = True

    return render(request, 'learnit/course-list.html', context=context)


def course_category(request):

    context = {}
    category = request.GET['c']
    try:
        cat = Category.objects.get(name=category)
        courses = Course.objects.filter(category=cat)
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

    context['searchx_count'] = courses.count()

    if courses.count() > 5:
        context['is_paginated'] = True

    return render(request, 'learnit/course-list.html', context=context)

# def course_tag(request):
#     context = {}
#     tag = request.GET['t']
#     try:
#         context['courses'] = Course.objects.filter(tag__icontains=tag)
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

def razor_payment(request):

    response = request.POST

    print(response)

    params_dict = {
        'razorpay_payment_id' : response['razorpay_payment_id'],
        'razorpay_order_id' : response['razorpay_order_id'],
        'razorpay_signature' : response['razorpay_signature']
    }
    # VERIFYING SIGNATURE
    try:
        status = client.utility.verify_payment_signature(params_dict)

        order_data = client.order.fetch(response['razorpay_order_id'])

        course_slug = order_data['notes']['course-slug']
        user = request.user

        course = Course.objects.get(slug=course_slug)
        sub = Subscription.objects.create(user=user, course=course)

        order_amount = order_data['amount']//100
        payment_id = response['razorpay_payment_id']
        order_currency = order_data['currency']
        order_id = response['razorpay_order_id']

        Payment.objects.create(amount=order_amount, subscription=sub, currency=order_currency, razorpay_payment_id=payment_id, razorpay_order_id=order_id)
        messages.success(request, 'Your course has been enrolled.')

        return redirect('my-courses')

    except:

        messages.error(request, 'Something went wrong, try again.')
        return redirect('courses-list')



def profile(request):
    return HttpResponse("Peofile of "+str(request.user.email))
