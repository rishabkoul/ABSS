import threading
import requests
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from account.forms import UserRegistrationForm, AccountAuthenticationForm, AccountUpdateForm
from registerform.models import RegistrationForm
from post.views import get_post_queryset_account
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
import random
from django.conf import settings
from django.http import HttpResponse
from account.models import Account

from post.models import Post

BLOG_POSTS_PER_PAGE = 10


class SMSThread(threading.Thread):

    def __init__(self, requests, url, headers, params):
        self.requests = requests
        self.url = url
        self.headers = headers
        self.params = params
        threading.Thread.__init__(self)

    def run(self):
        self.requests.request(
            "POST", self.url, headers=self.headers, params=self.params)


def registration_view(request):
    if request.user.is_authenticated:
        return redirect('home')
    context = {}
    if request.POST:
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            phone = form.cleaned_data.get('phone')
            raw_password = form.cleaned_data.get('password1')
            account = authenticate(phone=phone, password=raw_password)
            login(request, account)
            return redirect('home')
        else:
            context['registration_form'] = form
    else:
        form = UserRegistrationForm()
        context['registration_form'] = form
    return render(request, 'account/register.html', context)

# Create your views here.


def logout_view(request):
    logout(request)
    return redirect('home')


def login_view(request):
    context = {}

    user = request.user
    if user.is_authenticated:
        return redirect("home")

    if request.POST:
        form = AccountAuthenticationForm(request.POST)
        if form.is_valid():
            phone = request.POST['phone']
            password = request.POST['password']
            user = authenticate(phone=phone, password=password)

            if user:
                login(request, user)
                return redirect("home")

    else:
        form = AccountAuthenticationForm()

    context['login_form'] = form
    return render(request, 'account/login.html', context)


def account_view(request):

    if not request.user.is_authenticated:
        return redirect("login")

    registration = RegistrationForm.objects.filter(user=request.user)
    if registration:
        registration = registration[0]

    context = {}

    if request.POST:
        form = AccountUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.initial = {
                "email": request.POST['email'],
                "username": request.POST['username'],
                "phone": request.POST['phone'],
            }
            form.save()
            context['success_message'] = "Updated"
    else:
        form = AccountUpdateForm(
            initial={
                "email": request.user.email,
                "username": request.user.username,
                "phone": request.user.phone,
            }
        )
    context['account_form'] = form

    query = ''
    if request.GET:
        query = request.GET.get('q', '')
        context['query'] = str(query)

    posts = get_post_queryset_account(query, request.user)
    page = request.GET.get('page', 1)
    posts_paginator = Paginator(posts, BLOG_POSTS_PER_PAGE)

    try:
        posts = posts_paginator.page(page)
    except PageNotAnInteger:
        posts = posts_paginator.page(BLOG_POSTS_PER_PAGE)
    except EmptyPage:
        posts = posts_paginator.page(posts_paginator.num_pages)
    context['posts'] = posts

    context['registration'] = registration
    return render(request, 'account/account.html', context)


def sendotp(request, phone):
    otp = str(random.randint(1000, 9999))
    request.session['otp'] = otp

    mesagge = 'Your ABSS otp is '+otp
    querystring = {"from": "+13093160712", "body": mesagge,
                   "to": "+91"+str(phone)}
    SMSThread(requests, settings.SMS_URL,
              settings.SMS_HEADERS, querystring).start()
    return HttpResponse('')


def changepasswordview(request):
    if not request.user.is_authenticated:
        return redirect("login")

    context = {}

    if request.POST:
        if('otp' in request.session):
            if request.POST.get('otp') == request.session['otp']:
                return redirect('changepasswordform', request.user.phone, request.session['otp'])
            else:
                context['otperror'] = 'Wrong OTP'
        else:
            context['otperror'] = 'Send OTP First'

    return render(request, 'account/changepassword.html', context)


def changepasswordform(request, phone, otp):
    if('otp' in request.session):
        if otp == request.session['otp']:
            account = Account.objects.filter(phone=phone).first()
            context = {}
            if request.POST:
                account.set_password(request.POST.get('password'))
                account.save()
                context['message'] = 'Password Changed'

            return render(request, 'account/changepasswordform.html', context)
        else:
            return redirect('changepassword')
    else:
        return redirect('changepassword')


def resetpasswordview(request, phone):

    context = {}

    if request.POST:
        if('otp' in request.session):
            if request.POST.get('otp') == request.session['otp']:
                return redirect('changepasswordform', phone, request.session['otp'])
            else:
                context['otperror'] = 'Wrong OTP'
        else:
            context['otperror'] = 'Send OTP First'

    return render(request, 'account/resetpasswordview.html', context)


def resetpassword(request):

    context = {}

    if request.POST:
        if(Account.objects.filter(phone=request.POST.get('phone'))):
            return redirect('resetpasswordview', request.POST.get('phone'))
        else:
            context['message'] = 'Phone no does not exist'

    return render(request, 'account/resetpassword.html', context)
