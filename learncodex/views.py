from django.shortcuts import render
from django.http import HttpResponse

def index(request):

    return render(request,'learnit/home.html')

def courses(request):

    return render(request,'learnit/course-list.html')

def course_detail(request,course):

    return render(request,'learnit/single-course.html')

def course_learning(request,course,lesson):

    return render(request,'learnit/course-galary.html')


def profile(request):

    return HttpResponse("Peofile of "+str(request.user))