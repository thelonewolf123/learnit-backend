from django.shortcuts import render
from django.http import HttpResponse

def index(request):

    return HttpResponse('Home page')

def courses(request):

    return render(request,'learncodex/course-list.html')

def course_detail(request):

    return HttpResponse('Course detail page')

def course_learning(request,course,lesson):

    return render(request,'learncodex/course-galary.html')


def profile(request):

    return HttpResponse("Peofile of "+str(request.user))