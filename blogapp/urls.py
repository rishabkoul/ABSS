"""blogapp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.conf.urls import url
from django.urls import path, include
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from django.conf import settings
import os

from personal.views import (
    home_screen_view,
    returnassetlink,
)

from account.views import(
    registration_view,
    logout_view,
    login_view,
    account_view,
    changepasswordview,
    sendotp,
    changepasswordform,
    resetpassword,
    resetpasswordview,
)

from registerform.views import(
    create_subscription,
    load_district,
    load_subdistrict,
    load_postoffice,
    see_subscription,
    load_village,
)

from post.views import(
    show_feed,
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home_screen_view, name='home'),
    path('post/', include('post.urls', 'post')),
    path('register/', registration_view, name='register'),
    path('logout/', logout_view, name='logout'),
    path('login/', login_view, name='login'),
    path('account/', account_view, name='account'),
    path('subscribe/', create_subscription, name='subscribe'),
    path('see_subscription/', see_subscription, name='see_subscription'),
    path('ajax/load-district', load_district, name='load-district'),
    path('ajax/load-subdistrict', load_subdistrict, name='load-subdistrict'),
    path('ajax/load-postoffice', load_postoffice, name='load-postoffice'),
    path('ajax/load-village', load_village, name='load-village'),
    path('feed/', show_feed, name='feed'),
    path('.well-known/assetlinks.json', returnassetlink),
    path('changepassword/', changepasswordview, name='changepassword'),
    path('sendotp/<phone>', sendotp, name='sendotp'),
    path('changepasswordform/<phone>/<otp>',
         changepasswordform, name='changepasswordform'),
    path('resetpassword/', resetpassword, name='resetpassword'),
    path('resetpasswordview/<phone>', resetpasswordview, name='resetpasswordview'),

    path('', include('pwa.urls')),
    url(r'session_security/', include('session_security.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
