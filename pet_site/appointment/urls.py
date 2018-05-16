from . import views


from django.conf.urls import url


app_name = 'appointment'


urlpatterns = [

    url(r"(?P<pk>[0-9]+)/$", views.AppointDetailView.as_view(), name="appointment"),

    url(r"(?P<pk>[0-9]+)/create_appointment/$", views.AppointCreateView.as_view(), name="add_appoint"),

    url(r"(?P<pk>[0-9]+)/update_appoint/$", views.AppointUpdateView.as_view(), name="appoint_update"),

    url(r"(?P<pk>[0-9]+)/make_comment/$", views.AppointCommentView.as_view(), name="make_comment"),

    url(r"(?P<pk>[0-9]+)/(?P<client_pk>[0-9]+)/delete_appoint/$", views.AppointDeleteView.as_view(), name="appoint_delete"),

]
