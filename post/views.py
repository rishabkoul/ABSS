from django.shortcuts import render, redirect, get_object_or_404
from registerform.models import RegistrationForm
from post.models import Post
from operator import attrgetter
from post.forms import CreatePostForm, UpdatePostForm
from account.models import Account
from django.db.models import Q
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator

BLOG_POSTS_PER_PAGE = 10

# Create your views here.


def create_post_view(request):

    context = {}

    user = request.user
    if not user.is_authenticated:
        return redirect('login')

    registration = RegistrationForm.objects.filter(user=request.user)
    if not registration:
        return redirect('subscribe')
    if not registration[0].is_approved:
        return redirect('see_subscription')
    if registration[0].membertype != 'Life Member':
        return redirect('feed')

    form = CreatePostForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        obj = form.save(commit=False)
        author = Account.objects.filter(email=user.email).first()
        obj.author = author
        obj.save()
        return redirect('feed')

    context['form'] = form

    context['registration'] = registration[0]

    return render(request, 'post/create_post.html', context)


def edit_post_view(request, pk):
    context = {}

    user = request.user
    if not user.is_authenticated:
        return redirect('login')

    registration = RegistrationForm.objects.filter(user=request.user)
    if not registration:
        return redirect('subscribe')
    if not registration[0].is_approved:
        return redirect('see_subscription')
    if registration[0].membertype != 'Life Member':
        return redirect('feed')

    post = get_object_or_404(Post, pk=pk)

    if request.POST:
        form = UpdatePostForm(request.POST or None,
                              request.FILES or None, instance=post)
        if form.is_valid():
            obj = form.save(commit=False)
            if request.POST.get('clear_image_image'):
                obj.image = None
            if request.POST.get('clear_image_videofile'):
                obj.videofile = None
            obj.save()
            context['success_message'] = "Updated"
            post = obj

    form = UpdatePostForm(
        initial={
            'title': post.title,
            'body': post.body or '',
            'image': post.image or None,
            'videofile': post.videofile or None,
        }
    )
    context['form'] = form
    context['registration'] = registration[0]
    return render(request, 'post/edit_post.html', context)


def get_post_queryset(query=None):
    queryset = []
    queries = query.split(" ")
    for q in queries:
        posts = Post.objects.filter(
            Q(title__icontains=q) |
            Q(body__icontains=q)
        ).distinct()

        for post in posts:
            queryset.append(post)

    return list(set(queryset))


def get_post_queryset_account(query=None, account=None):
    queryset = []
    queries = query.split(" ")
    for q in queries:
        posts = Post.objects.filter(author=account).filter(
            Q(title__icontains=q) |
            Q(body__icontains=q)
        ).distinct()

        for post in posts:
            queryset.append(post)

    return list(set(queryset))


def show_feed(request):
    if not request.user.is_authenticated:
        return redirect('login')
    registration = RegistrationForm.objects.filter(user=request.user)
    if not registration:
        return redirect('subscribe')
    if not registration[0].is_approved:
        return redirect('see_subscription')

    context = {}
    context['registration'] = registration[0]

    query = ''
    if request.GET:
        query = request.GET.get('q', '')
        context['query'] = str(query)

    posts = sorted(get_post_queryset(query),
                   key=attrgetter('date_updated'), reverse=True)

    page = request.GET.get('page', 1)
    posts_paginator = Paginator(posts, BLOG_POSTS_PER_PAGE)

    try:
        posts = posts_paginator.page(page)
    except PageNotAnInteger:
        posts = posts_paginator.page(BLOG_POSTS_PER_PAGE)
    except EmptyPage:
        posts = posts_paginator.page(posts_paginator.num_pages)

    context['posts'] = posts

    return render(request, 'post/feed.html', context)


def delPost(request, pk):
    if not request.user.is_authenticated:
        return redirect('login')
    registration = RegistrationForm.objects.filter(user=request.user)
    if not registration:
        return redirect('subscribe')
    if not registration[0].is_approved:
        return redirect('see_subscription')
    post_ = Post.objects.filter(pk=pk)
    post_.delete()
    return redirect('feed')
