from django.forms import (
    ModelForm,
    DateField,
    DateInput,
    CharField,
    TextInput,
    Textarea
)
from .models import Patient


class DateInput(DateInput):
    input_type='date'

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
    date_of_birth = DateField(widget=DateInput)
    phone_number = CharField(max_length=20, widget=TextInput)
    address = CharField(widget=Textarea)