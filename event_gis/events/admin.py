from django.contrib.gis import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from django.db.models import get_models, get_app

for model in get_models(get_app('events')):
	try:
		admin.site.register(model, admin.OSMGeoAdmin)
	except AlreadyRegistered:
		pass