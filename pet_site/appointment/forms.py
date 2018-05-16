from django import forms
from .models import (Appointment, TimeBooked, Groomer)
from accounts.models import Dog




class AppointCreateForm(forms.ModelForm):

    class Meta:
        model = Appointment
        fields = ['dog', 'groomer', 'appointment_date', 'appointment_time', 'service_option']



        widgets = {
            'appointment_date': forms.DateInput(attrs={'id': 'datetimepicker12', 'placeholder': 'yyyy-mm-dd'})
        }

    def __init__(self, *args, **kwargs):
        self.current_user = kwargs.pop('user')

        super(AppointCreateForm, self).__init__(*args, **kwargs)
        if self.current_user:
            self.fields['dog'].queryset = Dog.objects.filter(master=self.current_user)



class AppointUpdateForm(forms.ModelForm):

    class Meta:
        model = Appointment
        fields = ['groomer', 'appointment_date', 'appointment_time', 'service_option']


        widgets = {
            'appointment_date': forms.DateInput(attrs={'id': 'datetimepicker12', 'placeholder': 'yyyy-mm-dd'})
        }


