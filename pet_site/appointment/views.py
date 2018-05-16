from django.shortcuts import render
from django.views.generic import (DetailView,
                                  UpdateView,
                                  DeleteView,
                                  CreateView)

from .models import Groomer, TimeBooked, Appointment
from accounts.models import Client, Dog
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse, reverse_lazy
from django.shortcuts import get_object_or_404
from .forms import AppointCreateForm, AppointUpdateForm

# Create your views here.


class AppointDetailView(DetailView):
    model = Appointment

    context_object_name = 'appointment_detail'

    def get_object(self, queryset=None):
        """
        Return the object the view is displaying.

        Require `self.queryset` and a `pk` or `slug` argument in the URLconf.
        Subclasses can override this to return any object.
        """
        # Use a custom queryset if provided; this is required for subclasses
        # like DateDetailView
        if queryset is None:
            queryset = self.get_queryset()

        # Next, try looking up by primary key.
        client = self.kwargs['pk']

        queryset = Appointment.objects.filter(client=client)


        if not queryset:
            context = {'client_pk': client, 'noAppoint': True}
            return context

        else:
            obj = []
            for each_query in queryset:
                obj.append(each_query)
            # obj = queryset
            return obj


class AppointCreateView(CreateView):
    model = Appointment
    form_class = AppointCreateForm

    def get_form_kwargs(self):
        # pass value to form

        self.client = get_object_or_404(Client, pk=self.request.session.get('current_client_pk'))
        kwargs = super(AppointCreateView, self).get_form_kwargs()
        kwargs['user'] = self.client



        return kwargs


    def dispatch(self, request, *args, **kwargs):


        self.client = get_object_or_404(Client, pk=kwargs['pk'])


        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        groomer_choice = form.cleaned_data['groomer']
        booked_date_choice = form.cleaned_data['appointment_date']
        booked_time_choice = form.cleaned_data['appointment_time']

        queryset = TimeBooked.objects.filter(groomer=groomer_choice, booked_date=booked_date_choice, booked_time=booked_time_choice)
        # this time is not booked
        if not queryset:
            model_booked_time = TimeBooked()
            model_booked_time.groomer = groomer_choice
            model_booked_time.booked_date = booked_date_choice
            model_booked_time.booked_time = booked_time_choice
            model_booked_time.save()
            appointment = form.save(commit=False)
            appointment.client = self.client
            return super(AppointCreateView, self).form_valid(form)
        else:
            return render(self.request, 'appointment/time_has_booked.html', {'client_pk': self.request.session.get('current_client_pk')})



class AppointUpdateView(UpdateView):
    model = Appointment
    form_class = AppointUpdateForm


class AppointCommentView(UpdateView):
    model = Appointment

    fields = ('appointment_comment',)



class AppointDeleteView(DeleteView):
    model = Appointment
    success_url = reverse_lazy('appointment:appointment')
    template_name = 'appointment/appointment_confirm_delete.html'

    def get_object(self, queryset=None):

        if queryset is None:
            queryset = self.get_queryset()

        client = self.kwargs['client_pk']
        appointment_pk = self.kwargs['pk']

        queryset = Appointment.objects.filter(client=client, pk=appointment_pk)


        if not queryset:
            return HttpResponse('No Such an appointment! ')
        else:

            context = {'client_pk': client, 'appointment_pk': appointment_pk}
            return context

        # Override the delete function to delete report Y from client X
        # Finally redirect back to the client X page with the list of reports

    def delete(self, request, *args, **kwargs):
        client = self.kwargs['client_pk']
        appointment_pk = self.kwargs['pk']

        current_appointment = get_object_or_404(Appointment, client=client, pk=appointment_pk)

        groomer_choice = current_appointment.groomer
        booked_date_choice = current_appointment.appointment_date
        booked_time_choice = current_appointment.appointment_time

        booked_time_exist = TimeBooked.objects.filter(groomer=groomer_choice, booked_date=booked_date_choice, booked_time=booked_time_choice)
        booked_time_exist.delete()

        appointExist = Appointment.objects.filter(client=client, pk=appointment_pk)
        appointExist.delete()




        return HttpResponseRedirect(reverse('appointment:appointment', kwargs={'pk': client}))