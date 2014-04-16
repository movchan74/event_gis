# coding=utf-8
from django.contrib.gis.db import models
from django.contrib.auth.models import User

class Event(models.Model):
	name = models.CharField(max_length=150)
	description = models.TextField()
	address = models.CharField(max_length=150)
	place = models.CharField(max_length=250, null=True, blank=True)
	location = models.PointField()
	event_type = models.ForeignKey('EventType')
	start_time = models.DateTimeField()
	end_time = models.DateTimeField()
	objects = models.GeoManager()
	user = models.ForeignKey(User, null=True, blank=True)

	def __unicode__(self):
		return self.name

	class Meta:
		unique_together = ("name", "start_time", "end_time")

class EventType(models.Model):
	name = models.CharField(max_length=150, unique=True)
	description = models.TextField(null=True, blank=True)

	def __unicode__(self):
		return self.name