import floppyforms as forms

class Map(forms.Form):
	poly = forms.gis.PolygonField(widget=forms.gis.BaseGMapWidget(attrs={
		'map_width': 600,
		'map_height': 400,
		'map_srid': 4326,
		'display_wkt': True,
	}))