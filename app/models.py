from django.db import models

from phonenumber_field.modelfields import PhoneNumberField

class Patient(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone_number = PhoneNumberField()
    date_of_birth = models.DateField()
    address = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class Message(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    message = models.CharField(max_length=1000)
    is_patient = models.BooleanField()
    sent_by_nurse = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.patient.first_name} {self.message[:20]}"

