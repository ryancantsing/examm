from __future__ import unicode_literals
from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from .models import Users, Trips
from django.db.models import Count


def index(request):
    return render(request, "exam5/index.html")
def travels(request):
    user = Users.objects.get(id=request.session['user_id'])
    joined_trips = user.joining_trip.all()
    other_trips = Trips.objects.exclude(trip_joiner=user)
    context = {
        'user' : user,
        'joined_trips' : joined_trips,
        'other_trips' : other_trips,
    }
    return render(request, "exam5/travels.html", context)
def register(request):
    result = Users.objects.validate_registration(request.POST)
    if type(result) == list:
        for err in result:
            messages.error(request, err)
        return redirect('/')
    else:
        request.session['user_id'] = result.id
        return redirect('/travels')
def destination(request, trip_id):
    trip = Trips.objects.get(id=trip_id)
    trip_joiners = trip.trip_joiner.annotate(people_joining = Count('id'))
    context = {
        'trip' : trip,
        'trip_joiners' : trip_joiners
    }
    return render(request, "exam5/destination.html", context)
def add(request):
    return render(request, "exam5/add.html")

def login(request):
    result = Users.objects.validate_login(request.POST)
    if type(result) == list:
        for err in result:
            messages.error(request, err)
        return redirect('/')
    request.session['user_id'] = result.id
    request.session['username'] = result.username
    return redirect('/travels')

def logout(request):
    del request.session['user_id']
    return redirect('/')
def create_trip(request):
    user= Users.objects.get(id=request.session['user_id'])
    result = Trips.objects.validate_trip(request.POST, user)
    if type(result) == list:
        for err in result:
            messages.error(request, err)
        return redirect('/add')
    else:     
        user.joining_trip.add(result.id)
        return redirect('/travels')
    return redirect('/')
def join_trip(request, trip_id):
    user=Users.objects.get(id=request.session['user_id'])
    user.joining_trip.add(trip_id)
    return redirect('/travels')
