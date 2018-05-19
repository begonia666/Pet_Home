from django import forms
from .models import (Client, Dog)
from django.forms import ValidationError




class UserSignUpForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ('email', 'password', 'user_name', 'home_address', 'mobile_phone', 'work_phone', 'home_phone')

        widgets = {

            'password': forms.PasswordInput(),
            'email': forms.EmailInput(attrs={'placeholder': 'user@gmail.com'}),
            'user_name': forms.TextInput(attrs={'placeholder': 'username'}),
            'home_address': forms.TextInput(attrs={'placeholder': '123 lython street'}),
            'mobile_phone': forms.TextInput(attrs={'placeholder': '+61123456789'}),
            'work_phone': forms.TextInput(attrs={'placeholder': '+61123456789'}),
            'home_phone': forms.TextInput(attrs={'placeholder': '+61123456789'}),
        }

        labels = {
            'email': 'Email (*required)',
            'user_name': 'Name',
            'password': 'Password (*required)',
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

        labels = {
            'dog_name': 'Dog Name (*required)',
            'dog_breed': 'Dog Breed (*required)'
        }


class DogUpdateForm(forms.ModelForm):

    class Meta:
        model = Dog
        exclude = ['master']

        widgets = {
            'dog_birth': forms.DateInput(attrs={'id': 'dog_birth_picker', 'placeholder': 'YYYY-MM-DD'})
        }

