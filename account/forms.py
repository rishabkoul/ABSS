from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate

from account.models import Account


class UserRegistrationForm(UserCreationForm):

    email = forms.EmailField(max_length=60, required=False)

    class Meta:
        model = Account
        fields = ("email", "username", "phone", "password1", "password2")


class AccountAuthenticationForm(forms.ModelForm):
    password = forms.CharField(label='Password', widget=forms.PasswordInput)

    class Meta:
        model = Account
        fields = ('phone', 'password')

    def clean(self):
        if self.is_valid():
            phone = self.cleaned_data['phone']
            password = self.cleaned_data['password']
            if not authenticate(phone=phone, password=password):
                raise forms.ValidationError("Invalid login")


class AccountUpdateForm(forms.ModelForm):

    class Meta:
        model = Account
        fields = ('email', 'username', 'phone')

    def clean_username(self):
        if self.is_valid():
            username = self.cleaned_data['username']
            try:
                account = Account.objects.exclude(
                    pk=self.instance.pk).get(username=username)
            except Account.DoesNotExist:
                return username
            raise forms.ValidationError(
                'Username "%s" is already in use.' % username)

    def clean_phone(self):
        if self.is_valid():
            phone = self.cleaned_data['phone']
            try:
                account = Account.objects.exclude(
                    pk=self.instance.pk).get(phone=phone)
            except Account.DoesNotExist:
                return phone
            raise forms.ValidationError(
                'Phone "%s" is already in use.' % phone)
