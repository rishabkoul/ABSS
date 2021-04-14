from django.shortcuts import render, redirect
from registerform.models import RegistrationForm

# Create your views here.


def home_screen_view(request):
    context = {}

    if request.user.is_authenticated:
        return redirect('feed')
    else:
        registration = None

    context = {
        'some_string': "this is some string that I'm passing to the view",
        'registration': registration,
    }

    return render(request, 'personal/home.html', context)


def returnassetlink(request):
    return render(request, '.well-known/assetlinks.json')
