from django.shortcuts import render, redirect
from registerform.models import RegistrationForm
from registerform.forms import RegistrationCreationFrom
from address.models import Address
from account.models import Account

# Create your views here.


def create_subscription(request):
    if not request.user.is_authenticated:
        return redirect('login')
    registration = RegistrationForm.objects.filter(user=request.user)

    if(registration):
        return redirect('see_subscription')

    form = RegistrationCreationFrom()
    if request.method == 'POST':
        form = RegistrationCreationFrom(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            user = Account.objects.filter(
                username=request.user.username).first()
            obj.user = user
            obj.save()
            return redirect('see_subscription')
    states = list(Address.objects.order_by(
        'state').values_list('state', flat=True).distinct())
    return render(request, 'registerform/register.html', {'form': form, 'states': states})


def see_subscription(request):
    if not request.user.is_authenticated:
        return redirect('login')
    registration = RegistrationForm.objects.filter(user=request.user)

    if(not registration):
        return redirect('subscribe')

    return render(request, 'registerform/see_registration.html', {'registration': registration[0]})


def load_district(request):
    if not request.user.is_authenticated:
        return redirect('login')
    registration = RegistrationForm.objects.filter(user=request.user)

    if(registration):
        return redirect('see_subscription')
    state = request.GET.get('state_id')
    districts = list(Address.objects.filter(state=state).order_by(
        'district').values_list('district', flat=True).distinct())
    return render(request, 'registerform/district_dropdown_list.html', {'districts': districts})


def load_subdistrict(request):
    if not request.user.is_authenticated:
        return redirect('login')
    registration = RegistrationForm.objects.filter(user=request.user)

    if(registration):
        return redirect('see_subscription')
    state = request.GET.get('state_id')
    district = request.GET.get('district_id')
    subdistricts = list(Address.objects.filter(state=state).filter(district=district).order_by(
        'subdistrict').values_list('subdistrict', flat=True).distinct())
    return render(request, 'registerform/subdistrict_dropdown_list.html', {'subdistricts': subdistricts})


def load_postoffice(request):
    if not request.user.is_authenticated:
        return redirect('login')
    registration = RegistrationForm.objects.filter(user=request.user)

    if(registration):
        return redirect('see_subscription')
    state = request.GET.get('state_id')
    district = request.GET.get('district_id')
    subdistrict = request.GET.get('subdistrict_id')
    postoffices = list(Address.objects.filter(state=state).filter(district=district).filter(
        subdistrict=subdistrict).order_by('officename').values_list('officename', flat=True).distinct())
    return render(request, 'registerform/postoffice_dropdown_list.html', {'postoffices': postoffices})


def load_village(request):
    if not request.user.is_authenticated:
        return redirect('login')
    registration = RegistrationForm.objects.filter(user=request.user)

    if(registration):
        return redirect('see_subscription')
    state = request.GET.get('state_id')
    district = request.GET.get('district_id')
    subdistrict = request.GET.get('subdistrict_id')
    postoffice = request.GET.get('postoffice_id')
    villages = list(Address.objects.filter(state=state).filter(district=district).filter(subdistrict=subdistrict).filter(
        officename=postoffice).order_by('villagename').values_list('villagename', flat=True).distinct())
    return render(request, 'registerform/village_dropdown_list.html', {'villages': villages})
