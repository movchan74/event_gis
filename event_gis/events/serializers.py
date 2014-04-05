# coding=utf-8
from rest_framework import serializers
from events.models import Event

class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ('id', 'name', 'description', 'address', 'location', 'event_type', 'start_time', 'end_time')   
