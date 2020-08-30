from django.shortcuts import render

import bleach

from django.http.response import StreamingHttpResponse, Http404
from django.shortcuts import render, redirect
from django.views.generic import ListView
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.contrib import messages

from .models import Post, Comment, Category, Tag, NewsLetter
from .forms import CommentForm


def blog_list(request):

    posts = Post.objects.all()
    context = {}
    page_number = request.GET.get('page')
    paginator = Paginator(posts, 5)

    categories = Category.objects.all()

    try:
        page_obj = paginator.get_page(page_number)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)

    context['posts'] = page_obj
    context['page_obj'] = page_obj
    context['categories'] = categories
    context['tags'] = Tag.objects.all()
    context['blog_nav'] = 'active'
    if posts.count() > 5:
        context['is_paginated'] = True

    return render(request, 'blogx/blog-home.html', context)


def search_blog(request):

    search = request.GET['q']
    context = {}
    context['searchx'] = search
    try:
        result = Post.objects.filter(title__icontains=search)
        categories = Category.objects.all()
    except Exception as e:
        print(e)
        raise Http404
    page_number = request.GET.get('page')
    paginator = Paginator(result, 5)
    try:
        page_obj = paginator.get_page(page_number)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)
    context['posts'] = page_obj
    context['page_obj'] = page_obj
    context['categories'] = categories
    context['tags'] = Tag.objects.all()
    context['search_count'] = result.count()
    if result.count() == 0:
        context['search_result_zero'] = 'No results found using Site search.'

    if result.count() > 5:
        context['is_paginated'] = True

    return render(request, 'blogx/blog-home.html', context)


def category_blog(request):

    search = request.GET['c']
    context = {}
    context['catx'] = search
    try:
        category = Category.objects.get(name=search)
        result = Post.objects.filter(category=category)
        categories = Category.objects.all()
    except Exception as e:
        print(e)
        raise Http404
    page_number = request.GET.get('page', 1)
    paginator = Paginator(result, 5)
    try:
        page_obj = paginator.get_page(page_number)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)
    context['posts'] = page_obj
    context['page_obj'] = page_obj
    context['categories'] = categories
    context['search_count'] = result.count()
    context['tags'] = Tag.objects.all()
    if result.count() == 0:
        context['search_result_zero'] = 'No results found using Site search.'

    if result.count() > 5:
        context['is_paginated'] = True

    return render(request, 'blogx/blog-home.html', context)


def tag_blog(request):

    search = request.GET['t']
    context = {}
    context['tagx'] = search
    try:
        result = Post.objects.filter(tags__icontains=search)
        categories = Category.objects.all()
        page_number = request.GET.get('page', 1)
    except Exception as e:
        print(e)
        raise Http404
    paginator = Paginator(result, 5)
    try:
        page_obj = paginator.get_page(page_number)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)
    context['posts'] = page_obj
    context['page_obj'] = page_obj
    context['categories'] = categories
    context['search_count'] = result.count()
    context['tags'] = Tag.objects.all()
    if result.count() == 0:
        context['search_result_zero'] = 'Content not found'

    if result.count() > 5:
        context['is_paginated'] = True

    return render(request, 'blogx/blog-home.html', context)


def single_blog(request, id):

    try:
        post = Post.objects.get(slug=id)
        comments = Comment.objects.filter(post=post)
        categories = Category.objects.all()
    except Exception as e:
        print(e)
        raise Http404
    context = {}

    context['comments'] = comments
    context['comment_count'] = comments.count()
    context['categories'] = categories
    context['post'] = post
    context['tags'] = post.tags.split(',')

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            if request.user.is_authenticated:
                name = bleach.clean(request.POST['name'])
            else:
                name = 'Anonymous'

            message = bleach.clean(form.cleaned_data['message'])
            try:
                Comment.objects.create(name=name, post=post, message=message)

                messages.success(request, "Your comment has been added.")
            except Exception as e:
                print(e)
                raise Http404

            return redirect('single_blog', id=id)
        else:
            messages.error(request, form.errors)
            context['form'] = form
            return redirect('single_blog', id)
    else:
        form = CommentForm()
        context['form'] = form
        return render(request, 'blogx/blog-post.html', context)


def news_letter(request):

    if request.method == 'POST':

        email = request.POST['email']
        NewsLetter.objects.create(email=email)
        messages.success(request, "Your E-mail has been successfuly added.")
        return redirect('index')

    else:
        raise Http404


def unsubscribe(request, uuid):

    try:
        user = NewsLetter.objects.get(uuid=uuid)
        user.delete()
    except Exception as e:
        print(e)
        messages.error(request, "Something went wrong, try again.")
        return redirect('index')
    messages.success(request, "Your E-mail has been successfully removed")
    return redirect('index')