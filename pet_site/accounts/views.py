from django.shortcuts import render
from .form import UserSignUpForm, DogForm, DogUpdateForm
from .models import Client, Dog
from django.views.generic import (View,
                                  TemplateView,
                                  CreateView,
                                  ListView,
                                  DetailView,
                                  DeleteView,
                                  UpdateView)

# login
from django.urls import reverse, reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect

# profile
from django.shortcuts import get_object_or_404
# Create your views here.



def login_home_page(request):
    isLogin = False
    valid_client = Client.objects.filter(email=request.session.get('current_email'), password=request.session.get('current_password'))
    if valid_client is not None:
        isLogin = True
        display_username = ''
        pk = ''
        for person in Client.objects.raw('SELECT * FROM accounts_client WHERE email=%s', [request.session.get('current_email')]):
            display_username = person.get_username()
            pk = person.get_pk()
        return render(request, 'base.html', {'isLogin': isLogin,
                                             'display_username': display_username,
                                             'user_pk': pk})
    else:
        return HttpResponse('Session is out of date, login again')


def register_page(request):
    registered = False

    if request.method == "POST":
        user_form = UserSignUpForm(data=request.POST)
        dog_form = DogForm(data=request.POST)

        if user_form.is_valid() and dog_form.is_valid():
            user = Client()
            user.email = user_form.cleaned_data['email']
            user.password = user_form.cleaned_data['password']
            user.user_name = user_form.cleaned_data['user_name']
            user.home_address = user_form.cleaned_data['home_address']
            user.home_phone = user_form.cleaned_data['home_phone']
            user.work_phone = user_form.cleaned_data['work_phone']
            user.mobile_phone = user_form.cleaned_data['mobile_phone']

            user.save()
            dog = Dog()
            dog.master = user
            dog.dog_name = dog_form.cleaned_data['dog_name']
            dog.dog_breed = dog_form.cleaned_data['dog_breed']
            dog.dog_birth = dog_form.cleaned_data['dog_birth']
            dog.dog_description = dog_form.cleaned_data['dog_description']
            dog.save()

            registered = True
        else:
            HttpResponse(user_form.errors, dog_form.errors)

    else:
        user_form = UserSignUpForm()
        dog_form = DogForm()

    return render(request, 'accounts/register.html', {
        'user_form': user_form,
        'dog_form': dog_form,
        'isRegister': registered
    })


def login_page(request):
    isLogin = False
    if request.method == "POST":
        email = request.POST.get('userEmail')
        password = request.POST.get('userPassword')
        valid_client = Client.objects.filter(email=email, password=password)

        if len(valid_client) == 1:

            request.session['current_email'] = email
            request.session['current_password'] = password
            isLogin = True
            display_username = ''
            pk = ''
            for person in Client.objects.raw('SELECT * FROM accounts_client WHERE email=%s', [email]):
                display_username = person.get_username()
                pk = person.get_pk()
                request.session['current_client_pk'] = pk
            return render(request, 'base.html', {'isLogin': isLogin,
                                                 'display_username': display_username,
                                                 'user_pk': pk})
        else:
            return render(request, 'accounts/login_fail.html')

    else:
        return render(request, 'accounts/login.html', {'isLogin': isLogin})


@login_required()
def logout_page(request):
    logout(request)
    return HttpResponseRedirect(reverse('home_page'))


class UserDetailView(DetailView, LoginRequiredMixin):
    context_object_name = 'client_details'
    model = Client
    # template_name = 'accounts/client_detail.html'


class DogCreateView(CreateView, LoginRequiredMixin):
    model = Dog
    # fields = ('dog_name', 'dog_breed', 'dog_birth', 'dog_description')
    form_class = DogForm
    def dispatch(self, request, *args, **kwargs):


        self.client = get_object_or_404(Client, pk=kwargs['pk'])

        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):

        dog = form.save(commit=False)
        dog.master = self.client

        return super(DogCreateView, self).form_valid(form)


class DogUpdateView(UpdateView, LoginRequiredMixin):
    model = Dog
    form_class = DogUpdateForm




class DogDeleteView(DeleteView, LoginRequiredMixin):
    model = Dog
    success_url = reverse_lazy('accounts:profile')
    template_name = 'accounts/dog_confirm_delete.html'

    def get_object(self, queryset=None):

        if queryset is None:
            queryset = self.get_queryset()

        client = self.kwargs['pk']
        dog = self.kwargs['dog_pk']
        dog_name = self.kwargs['dogname']
        user_name = self.kwargs['username']

        queryset = Dog.objects.filter(master=client, pk=dog)

        if not queryset:
            return HttpResponse('No Such a Dog! ')
        else:

            context = {'client_pk': client, 'dog_id': dog, 'dog_name': dog_name, 'username': user_name}
            return context

        # Override the delete function to delete report Y from client X
        # Finally redirect back to the client X page with the list of reports

    def delete(self, request, *args, **kwargs):
        client = self.kwargs['pk']
        dog = self.kwargs['dog_pk']


        dogExist = Dog.objects.filter(master=client, id=dog)
        dogExist.delete()

        return HttpResponseRedirect(reverse('accounts:profile', kwargs={'pk': client}))



class UserUpdateView(UpdateView, LoginRequiredMixin):
    model = Client
    fields = ('user_name', 'home_address', 'mobile_phone', 'work_phone', 'home_phone')


