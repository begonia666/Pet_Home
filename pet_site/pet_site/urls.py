"""pet_site URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.conf.urls import url, include
from . import views
from django.core.mail import send_mail


urlpatterns = [
    url('admin/', admin.site.urls),

    url(r'^$', views.HomePage.as_view(), name='home_page'),

    url(r'^accounts/', include('accounts.urls', namespace='accounts')),

    url(r'^appointment/', include('appointment.urls', namespace='appointment')),


]


def send(appoint):
    subject = 'Tom\'s Dog Grooming remind'
    message = 'Hello dear %s,\n\n' \
              'Your dog grooming appointment is coming in 24 hours!\n\n' \
              'Time: %s\n\n' \
              'Dog Name: %s\n\n' \
              'Groom option: %s\n\n' \
              'Regards,\n\n' \
              'Tom\'s Dog Grooming' % (
                  appoint.client.user_name,
                  str(appoint.appointment_date)+' '+str(appoint.appointment_time),
                  appoint.dog.dog_name,
                  appoint.get_service_option_display(),
              )
    to = [appoint.client.email]
    print('Sent email to! %s (%s)' % (appoint.client.user_name, appoint.client.email))
    send_mail(subject, message, 'toms-pet-home@hotmail.com', to, fail_silently=True)


def start_mail_thread():
    from threading import Thread
    from appointment.models import Appointment
    from datetime import timedelta
    from time import sleep
    from django.utils import timezone
    import datetime
    import pandas
    import pytz

    def worker_func():
        utc = pytz.UTC
        while True:
            now = timezone.now()
            next23 = now + timedelta(hours=23)
            next24 = now + timedelta(hours=24)

            for appoint in Appointment.objects.all():
                my_appoint = pandas.to_datetime(appoint.appointment_date.strftime('%Y%m%d') + appoint.appointment_time.strftime('%H%M'), format="%Y%m%d%H%M")
                my_appoint = utc.localize(my_appoint)

                if next23 < my_appoint < next24:
                   
                    send(appoint)

            # Sleep 1 hour
            sleep(60 * 60)

    worker = Thread(target=worker_func, daemon=True)
    worker.start()


start_mail_thread()