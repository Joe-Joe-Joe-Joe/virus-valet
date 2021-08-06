from django.db import models

class Patient(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=12)
    date_of_birth = models.DateField()
    address = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
