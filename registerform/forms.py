from django import forms
from django.forms import Form
from django.forms import CharField,TextInput
from address.models import Address
from registerform.models import RegistrationForm

class RegistrationFormSearch(Form):
    state=CharField(required=False,widget=TextInput(
        attrs={
            'filter_method':'__icontains'
        }
    ))
    district=CharField(required=False,widget=TextInput(
        attrs={
            'filter_method':'__icontains'
        }
    ))
    subdistrict=CharField(required=False,widget=TextInput(
        attrs={
            'filter_method':'__icontains'
        }
    ))
    postoffice=CharField(required=False,widget=TextInput(
        attrs={
            'filter_method':'__icontains'
        }
    ))
    village=CharField(required=False,widget=TextInput(
        attrs={
            'filter_method':'__icontains'
        }
    ))

class RegistrationCreationFrom(forms.ModelForm):
    class Meta:
        model=RegistrationForm
        fields = ['membertype','membercategory','area','state','district','subdistrict','postoffice','village','templename']

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.fields['state'].queryset=list(Address.objects.order_by('state').values_list('state',flat=True).distinct())
        self.fields['district'].queryset=Address.objects.none()
        self.fields['subdistrict'].queryset=Address.objects.none()
        self.fields['postoffice'].queryset=Address.objects.none()
        self.fields['village'].queryset=Address.objects.none()

        if 'state' in self.data:
            try:
                state=self.data.get('state_id')
                self.fields['district'].queryset=list(Address.objects.filter(state=state).order_by('district').values_list('district',flat=True).distinct())
            except(ValueError,TypeError):
                pass

            if 'district' in self.data:
                try:
                    state=self.data.get('state_id')
                    district=self.data.get('district_id')
                    self.fields['subdistrict'].queryset=list(Address.objects.filter(state=state).filter(district=district).order_by('subdistrict').values_list('subdistrict',flat=True).distinct())
                except(ValueError,TypeError):
                    pass

                if 'subdistrict' in self.data:
                    try:
                        state=self.data.get('state_id')
                        district=self.data.get('district_id')
                        subdistrict=self.data.get('subdistrict_id')
                        self.fields['postoffice'].queryset=list(Address.objects.filter(state=state).filter(district=district).filter(subdistrict=subdistrict).order_by('officename').values_list('officename',flat=True).distinct())
                    except(ValueError,TypeError):
                        pass

                    if 'postoffice' in self.data:
                        try:
                            state=self.data.get('state_id')
                            district=self.data.get('district_id')
                            subdistrict=self.data.get('subdistrict_id')
                            postoffice=self.data.get('postoffice_id') 
                            self.fields['village'].queryset=list(Address.objects.filter(state=state).filter(district=district).filter(subdistrict=subdistrict).filter(officename=postoffice).order_by('villagename').values_list('villagename',flat=True).distinct())
                        except(ValueError,TypeError):
                            pass