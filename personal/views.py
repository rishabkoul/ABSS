from django.shortcuts import render
from registerform.models import RegistrationForm

# Create your views here.


def home_screen_view(request):
    context = {}

    if request.user.is_authenticated:
        registration = RegistrationForm.objects.filter(user=request.user)
        if registration:
            registration = registration[0]
    else:
        registration = None

    context = {
        'some_string': "this is some string that I'm passing to the view",
        'registration': registration,
    }

    return render(request, 'personal/home.html', context)


def returnassetlink(request):
    return render(request, '.well-known/assetlinks.json')
