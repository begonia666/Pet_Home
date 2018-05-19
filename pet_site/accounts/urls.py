from . import views


from django.conf.urls import url


app_name = 'accounts'


urlpatterns = [

    url(r"login_home/$", views.login_home_page, name="login_home"),

    url(r"signup/$", views.register_page, name="signup"),

    url(r"login/$|login_home/$", views.login_page, name="login"),

    url(r"logout/$", views.logout_page, name="logout"),

    url(r"(?P<pk>[0-9]+)/$", views.UserDetailView.as_view(), name="profile"),

    url(r"(?P<pk>[0-9]+)/create_dog/$", views.DogCreateView.as_view(), name="add_dog"),

    url(r"(?P<pk>[0-9]+)/update_dog/$", views.DogUpdateView.as_view(), name="dog_update"),

    url(r"(?P<pk>[0-9]+)/(?P<dog_pk>[0-9]+)/(?P<dogname>\S+)/delete_dog/$", views.DogDeleteView.as_view(), name="dog_delete"),

    url(r"(?P<pk>[0-9]+)/update_user/$", views.UserUpdateView.as_view(), name="profile_update"),
]
