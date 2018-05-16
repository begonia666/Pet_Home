from django.db import models

from phonenumber_field.modelfields import PhoneNumberField
from django.urls import reverse


# Create your models here.

# client part
class Client(models.Model):
    email = models.EmailField(blank=False, unique=True)
    password = models.CharField(max_length=50, blank=False)
    user_name = models.CharField(blank=True, max_length=50)
    home_address = models.CharField(blank=True, max_length=300)
    mobile_phone = PhoneNumberField(blank=True)
    work_phone = PhoneNumberField(blank=True)
    home_phone = PhoneNumberField(blank=True)

    def get_username(self):
        return self.user_name

    def get_pk(self):
        return self.pk

    def __str__(self):
        return self.email

    def get_absolute_url(self):
        return reverse('accounts:profile', kwargs={'pk': self.pk})






class Dog(models.Model):

    master = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='dog_for_user')

    dog_name = models.CharField(max_length=50, blank=False)

    dog_breed = models.IntegerField(blank=False, choices=[
        (1, 'Affenpinscher'),
        (2, 'Afghan Hound'),
        (3, 'Airedale Terrier'),
        (4, 'Akita'),
        (5, 'Alaskan Malamute'),
        (6, 'American Cocker Spaniel'),
        (7, 'American Eskimo Dog (Miniature)'),
        (8, 'etc')
    ])

    dog_birth = models.DateField(null=True, blank=True)

    dog_description = models.CharField(blank=True, max_length=300)

    def __str__(self):
        return self.dog_name

    def get_absolute_url(self):
        return reverse('accounts:profile', kwargs={'pk': self.master.pk})








