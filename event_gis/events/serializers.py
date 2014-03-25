# coding=utf-8
from rest_framework import serializers
from events.models import Event

class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ('id', 'name', 'location')
   
class EventInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ('id', 'name', 'description', 'address', 'location', 'event_type', 'start_time', 'end_time')
        #TODO: вместо объекта event_type нужно возвращать строку с наименованием типа
        