from django import forms
from .models import (Client, Dog)
from django.forms import ValidationError




class UserSignUpForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ('email', 'user_name', 'password', 'home_address', 'mobile_phone', 'work_phone', 'home_phone')

        widgets = {

            'password': forms.PasswordInput()
        }

        labels = {
            'user_name': 'Name'
        }

    def clean_email(self):
        email = self.cleaned_data['email']
        if Client.objects.filter(email=email).count() > 0:
            raise ValidationError('This email address is already used!')
        return email.lower()


class DogForm(forms.ModelForm):
    # id = forms.IntegerField(widget=forms.HiddenInput())

    class Meta:
        model = Dog
        exclude = ['master']

        widgets = {
            'dog_birth': forms.DateInput(attrs={'id': 'dog_birth_picker', 'placeholder': 'YYYY-MM-DD'})
        }


class DogUpdateForm(forms.ModelForm):

    class Meta:
        model = Dog
        exclude = ['master']

        widgets = {
            'dog_birth': forms.DateInput(attrs={'id': 'dog_birth_picker', 'placeholder': 'YYYY-MM-DD'})
        }

