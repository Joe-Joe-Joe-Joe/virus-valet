from django.db import models

from phonenumber_field.modelfields import PhoneNumberField



class Patient(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone_number = PhoneNumberField()
    date_of_birth = models.DateField()
    address = models.CharField(max_length=50)

    finished_chat = models.BooleanField(default = False)
    dying = models.BooleanField(default = False)

    def __str__(self):
        return f"{self.first_name} {self.last_name} MODEL"


class UserData(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    is_symptomatic = models.BooleanField(default = False)
    not_isolating = models.BooleanField(default = False)
    attending_public = models.BooleanField(default = False)


class Message(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    message = models.CharField(max_length=1000)
    is_patient = models.BooleanField()
    is_question = models.BooleanField()
    is_answer = models.IntegerField()
    sent_by_nurse = models.BooleanField(default=False)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.patient.first_name} {self.message[:20]} patient:{self.is_patient} question:{self.is_question} answer:{self.is_answer} sent"

