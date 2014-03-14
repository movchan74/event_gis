import floppyforms as forms

class Map(forms.Form):
    poly = forms.gis.PolygonField(widget=forms.gis.BaseGMapWidget(attrs={
        'map_width': 1000,
        'map_height': 700,
    }))