# coding=utf-8
from django.contrib.gis.db import models
from django.contrib.auth.models import User

class Event(models.Model):
	name = models.CharField(max_length=150)
	description = models.TextField()
	address = models.CharField(max_length=150)
	location = models.PointField()
	event_type = models.ForeignKey('EventType')
	start_time = models.DateTimeField()
	end_time = models.DateTimeField()
	objects = models.GeoManager()
	user = models.ForeignKey(User, null=True)

class EventType(models.Model):
	name = models.CharField(max_length=150)
	description = models.TextField()