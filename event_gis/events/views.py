from django.shortcuts import render_to_response
from django.template import RequestContext
from forms import Map

def render_main_page(request):
	m = Map()
	return render_to_response('main_page.html', {'map_form' : m}, context_instance=RequestContext(request))



# from rest_framework import generics
# from events.serializers import EventSerializer

# class REST_DummyView(generics.ListAPIView):
#     serializer_class = EventSerializer

#     def get_queryset(self):
#         return Quest.objects.all() #TODO

from rest_framework.views import APIView
from rest_framework.response import Response

class REST_DummyView(APIView):
    def get(self, request, format=None):
        usernames = ['tratata', 'kekeke', 'alalala']
        return Response(usernames)