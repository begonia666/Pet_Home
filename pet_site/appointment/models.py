from django.db import models
from accounts.models import Client, Dog
from phonenumber_field.modelfields import PhoneNumberField
from django.urls import reverse
import datetime

# Create your models here.


class Groomer(models.Model):
    groomer_name = models.CharField(max_length=50, blank=False)

    groomer_phone = PhoneNumberField(blank=False)

    def __str__(self):
        return self.groomer_name






class TimeBooked(models.Model):
    groomer = models.ForeignKey(Groomer, on_delete=models.CASCADE, related_name='time_of_groomer')

    booked_date = models.DateField()

    booked_time = models.TimeField()

    def __str__(self):
        return str(self.booked_time)







class Appointment(models.Model):

    client = models.ForeignKey(Client, blank=False, on_delete=models.CASCADE)

    dog = models.ForeignKey(Dog, blank=False, on_delete=models.CASCADE, related_name='dog_appoint')

    groomer = models.ForeignKey(Groomer, on_delete=models.CASCADE, blank=False, related_name='groomer_of_appointment')

    appointment_date = models.DateField(blank=False, null=False)

    appointment_time = models.TimeField(choices=[
        (datetime.time(10,00,00), datetime.time(10,00,00)),
        (datetime.time(11,30,00), datetime.time(11,30,00)),
        (datetime.time(13,00,00), datetime.time(13,00,00)),
        (datetime.time(14,30,00), datetime.time(14,30,00)),
        (datetime.time(16,00,00), datetime.time(16,00,00)),

    ], blank=False, null=False)



    service_option = models.IntegerField(choices=[
        (1, 'wash only'),
        (2, 'wash and nail clipping'),
        (3, 'deluxe grooming'),
        (4, 'etc')
    ], blank=False)


    appointment_comment = models.CharField(blank=True, max_length=300)


    def get_absolute_url(self):
        return reverse('appointment:appointment', kwargs={'pk': self.client.pk})

    def __str__(self):
        return str(self.appointment_date) + ' ' + str(self.appointment_time)