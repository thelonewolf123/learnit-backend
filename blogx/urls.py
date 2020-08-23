from django.urls import path
from . import views

urlpatterns = [
    path('', views.blog_list, name='blog'),
    path('article/<slug:id>', views.single_blog, name='single_blog'),
    path('search/', views.search_blog, name='search_blog'),
    path('category/', views.category_blog, name='category_blog'),
    path('tag/', views.tag_blog, name='tag_blog'),
    path('news_letter/', views.news_letter, name='news-letter'),
    path('unsubscribe/<uuid>/', views.unsubscribe, name='unsubscribe'),

]
