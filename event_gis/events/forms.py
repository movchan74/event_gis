<<<<<<< HEAD
=======
import floppyforms as forms
 
class PointWidget(forms.gis.BaseGMapWidget, forms.gis.PointWidget):
	template_name = 'forms/google_map.html'
	default_lon = '37.6461231656120958'
	default_lat = '55.7572258153171276'

	def get_context_data(self):
		ctx = super(PointWidget, self).get_context_data()
		ctx.update({
			'lon': self.default_lon,
			'lat': self.default_lat,
		})
		return ctx
 
class Map(forms.Form):
	poly = forms.gis.PolygonField(widget=PointWidget(attrs={
		'map_width': 600,
		'map_height': 400,
		'map_srid': 4326,
		'display_wkt': True,
	}))

# May be useful in the future:

# class Map(forms.Form):

# 	# class BaseGMapWidget(forms.gis.BaseGeometryWidget):
# 	# 	map_srid = 900913  # Use the google projection
# 	# 	template_name = 'forms/google_map.html'
# 	# 	map_width = 600
# 	# 	map_height = 400
# 	# 	display_wkt = True

# 	# 	class Media:
# 	# 		js = (
# 	# 			'http://openlayers.org/dev/OpenLayers.js',
# 	# 			'floppyforms/js/MapWidget.js',
# 	# 			'http://maps.google.com/maps/api/js?sensor=false',
# 	# 		)
	
# 	poly = forms.gis.PolygonField(widget=forms.gis.BaseGMapWidget(attrs={
# 		'map_width': 600,
# 		'map_height': 400,
# 		'map_srid': 900913,
# 		'display_wkt': True,
# 		# 'default_lon': '55.7572258153171276',
# 		# 'default_lat': '37.6461231656120958',
# 		'default_lon': '4187526.1569922',
# 		'default_lat': '7517653.0919326',
# 		# 'template_name': 'forms/google_map.html',
# 	}))

# 	# class Media:
# 	# 	js = (
# 	# 		'http://openlayers.org/dev/OpenLayers.js',
# 	# 		'floppyforms/js/MapWidget.js',
# 	# 		'http://maps.google.com/maps/api/js?sensor=false',
# 	# 	)


# 	# poly = forms.gis.PolygonField(widget=GMapPolygonWidget(attrs={
# 	# 	'map_width': 600,
# 	# 	'map_height': 400,
# 	# 	'map_srid': 4326,
# 	# 	'display_wkt': True,
# 	# 	'template_name': 'forms/google_map.html',
# 	# }))

# 	# class PointWidget(forms.gis.BaseGMapWidget, forms.gis.PointWidget):
# 	# 	template_name = 'forms/google_map.html'
# 	# 	default_lon = '55.7572258153171276'
# 	# 	default_lat = '37.6461231656120958'
# 	# 	map_srid = 4326  # Use the google projection
# 	# 	map_width = 600
# 	# 	map_height = 400
# 	# 	display_wkt = True

# 	# 	def get_context_data(self):
# 	# 		ctx = super(PointWidget, self).get_context_data()
# 	# 		ctx.update({
# 	# 			'lon': self.default_lon,
# 	# 			'lat': self.default_lat,
# 	# 		})
# 	# 		return ctx
>>>>>>> 70ea463eb6782d2822ce098cdb59dd8b4a740e03
