from django.conf.urls import url
from . import views           # This line is new!

urlpatterns = [
    url(r'^$', views.index),     # This line has changed!
    url(r'^travels$', views.travels),     # This line has changed!
    url(r'^destination/(?P<trip_id>\d+)$', views.destination),
    url(r'^travels/add$', views.add),
    url(r'^create_trip$', views.create_trip),
    url(r'^join_trip/(?P<trip_id>\d+)$', views.join_trip),
    url(r'^login$', views.login),
    url(r'^logout$', views.logout),
    url(r'^register$', views.register),


  ]
