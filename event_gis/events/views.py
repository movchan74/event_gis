from django.shortcuts import render_to_response
from django.template import RequestContext
from forms import Map

def render_main_page(request):
	m = Map()
	return render_to_response('main_page.html', {'map_form' : m}, context_instance=RequestContext(request))