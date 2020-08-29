from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('courses/', views.courses, name='courses-list'),
    path('course/<slug:course>', views.course_detail, name='course-detail'),
    path('course/<slug:course>/enroll',
         views.course_enroll, name='course-enroll'),
    path('learn/course/<slug:course>',
         views.course_learning, name='course-learn'),
    path('my-courses/', views.my_courses, name='my-courses'),
    # path('tag/',views.course_tag,name='course-tag'),
    path('category/', views.course_category, name='course-category'),
    path('search/', views.course_search, name='course-search'),
    path('ask_inst/', views.ask_instructor, name='course-ask'),
    path('payment/',views.razor_payment,name='payment_status'),
]
