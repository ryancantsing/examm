from __future__ import unicode_literals
import re
import bcrypt
from django.db import models
from datetime import datetime

NAME_REGEX = re.compile(r'^[A-Za-z]\w+$')

class UserManager(models.Manager):
    def validate_login(self, post_data):
        errors = []
        # check DB for post_data['email']
        if len(self.filter(username=post_data['username'])) > 0:
            # check this user's password
            user = self.filter(username=post_data['username'])[0]
            if not bcrypt.checkpw(post_data['password'].encode(), user.password.encode()):
                errors.append('username/password incorrect')
        else:
            errors.append('username/password incorrect')

        if errors:
            return errors
        return user

    def validate_registration(self, post_data):
        errors = []
        if len(post_data['name']) < 2 or len(post_data['username']) < 2:
            errors.append("name fields must be at least 3 characters")
        if len(post_data['password']) < 8:
            errors.append("password must be at least 8 characters")
        if not re.match(NAME_REGEX, post_data['name']) or not re.match(NAME_REGEX, post_data['username']):
            errors.append('name fields must be letter characters only')
        if len(Users.objects.filter(username=post_data['username'])) > 0:
            errors.append("username already in use")
        if post_data['password'] != post_data['password_confirm']:
            errors.append("passwords do not match")

        if not errors:
            # make our new user
            # hash password
            hashed = bcrypt.hashpw((post_data['password'].encode()), bcrypt.gensalt(5))

            new_user = self.create(
                name=post_data['name'],
                username=post_data['username'],
                password=hashed
            )
            return new_user
        return errors
class TripManager(models.Manager):
    def validate_trip(self, post_data, user):
        errors = []
        if len(post_data['destination']) < 3:
            errors.append("Name of Destination must be at least 3 characters!")
        if len(post_data['description']) < 8:
            errors.append("Description must be at least 8 characters!")
        if len(Trips.objects.filter(destination=post_data['destination'])) > 0:
            errors.append("Trip has already been added!")
        if not(post_data['start_date']) or not(post_data['end_date']):
            errors.append("You must have a start date and end date!")
        if len(user.trip_organizer.filter(trip_start=post_data['start_date'])) > 0:
            errors.append("You have an overlapping trip!")
        if not errors:
            new_trip = self.create(
                destination=post_data['destination'],
                description=post_data['description'],
                added_by = user,
                trip_start=post_data['start_date'],
                trip_end=post_data['end_date']
            )
            return new_trip
        return errors

class Users(models.Model):
    name = models.CharField(max_length=255)
    username = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()
    def __str__(self):
        return self.username
class Trips(models.Model):
    destination = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    trip_start = models.DateField()
    trip_end = models.DateField()
    added_by = models.ForeignKey(Users, related_name="trip_organizer")
    trip_joiner = models.ManyToManyField(Users, related_name="joining_trip")
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = TripManager()
    def __str__(self):
        return self.destination