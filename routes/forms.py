from django import forms
from .models import Task
from decimal import Decimal

class TaskForm(forms.ModelForm):
        class Meta:
            model = Task
            fields = ['title', 'description', 'date', 'time', "lat", "lon" ]
            widgets = {
                    "lat" : forms.NumberInput( attrs={ "id": "lat", "step":str(Decimal('0.00000000000000000001'))} ),
                    "lon" : forms.NumberInput( attrs={ "id": "lon", "step":str(Decimal('0.00000000000000000001'))} )
                    }

