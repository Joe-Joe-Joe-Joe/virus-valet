from django.forms import ModelForm
from .models import Patient

class PatientForm(ModelForm):
    class Meta:
        model = Patient
        fields = [
            'first_name',
            'last_name',
            'phone_number',
            'date_of_birth',
            'address'
        ]