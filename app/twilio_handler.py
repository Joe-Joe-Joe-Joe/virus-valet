import os
from twilio.rest import Client
from .models import (Patient, Message)


class RecieveSend:
    def __init__(self):
        values = open("/home/blueuser/PycharmProjects/virus-valet/secrets.hidden", "r").read().split()
        self.sid = values[0]
        self.token = values[1]
        self.client = Client(self.sid, self.token)
        self.default_number = "+12262708145"

    def send_message(self, body, number_to, number_from = None):
        if number_from is None:
            number_from = self.default_number
        message = self.client.messages \
            .create(
            body=body,
            from_=number_from,
            to=number_to
        )

    def save_messages(self, request, is_patient):
        pull = lambda x : request.POST.get(x)
        body = pull("Body")
        phone_number = pull("From")
        patient = Patient.objects.filter(phone_number = phone_number)[0]
        message = Message(patient = patient, message = body, is_patient = is_patient)

        message.save()



if __name__ == "__main__":
    inter = SeRe()
    inter.send_message("message content", '+15191234123')
