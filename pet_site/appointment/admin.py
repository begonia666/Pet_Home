from django.contrib import admin
from .models import Appointment, TimeBooked, Groomer

# Register your models here.

class AppointmentAdmin(admin.ModelAdmin):

    fields = ['appointment_date', 'appointment_time', 'service_option', 'client', 'dog', 'groomer', 'appointment_comment']

    search_fields = ['appointment_date', 'appointment_time']

    list_filter = ['appointment_date', 'appointment_time', 'service_option', 'client', 'appointment_comment']

    list_display = ['appointment_date', 'appointment_time', 'service_option', 'client', 'appointment_comment']





admin.site.register(Appointment, AppointmentAdmin)
admin.site.register(TimeBooked)
admin.site.register(Groomer)

