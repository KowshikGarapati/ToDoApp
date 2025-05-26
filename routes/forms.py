from django import forms
from .models import Task
from decimal import Decimal
from django.utils import timezone

#insertion comment

class TaskForm(forms.ModelForm):
        class Meta:
            model = Task
            fields = ['title', 'description', 'date', 'time', "lat", "lon" ]
            widgets = {
                    "lat" : forms.NumberInput( attrs={ "id": "lat", "step":str(Decimal('0.00000000000000000001'))} ),
                    "lon" : forms.NumberInput( attrs={ "id": "lon", "step":str(Decimal('0.00000000000000000001'))} ),
                    'date': forms.DateInput(attrs={'type': 'date','class': 'form-control'}),
                    'time': forms.TimeInput(attrs={'type': 'time','class': 'form-control'})
                    }



        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.fields['date'].initial = timezone.now().date()
