from django.urls import path
from . import views

urlpatterns = [
    path('',views.index,name='index'),
    path('courses/',views.courses,name='courses-list'),
    path('course/<slug:course>',views.course_detail,name='course-detail'),
    path('course/<slug:course>/<slug:lesson>',views.course_learning,name='course-learn'),   
] 