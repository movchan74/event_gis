# coding=utf-8
from rest_framework import serializers
from events.models import Event, EventType

class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ('id', 'name', 'description', 'address', 'location', 'event_type', 'start_time', 'end_time')   

class EventTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventType
        fields = ('id', 'name', 'description')   

