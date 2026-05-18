from django import forms
from .models import Appointment 

class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ["service", "date", "time", "notes"]
        widgets = {
            "date": forms.DateInput(
                attrs={
                    "type": "date",
                    "min": "", 
                }
            ),
            "time": forms.TimeInput(
                attrs={
                    "type": "time"
                }
            ),
            "notes": forms.Textarea(
                attrs={
                    "rows": 3
                }
            )
        }