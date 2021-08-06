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
        self.questions = {
            "How are you?" : ["good", "bad", "alright", "shitty"],
            "What's up?" : ["nothing", "yes"],
            "Are you sad?" : ["yes", "no"]
        }
    def clear_messages(self):
        for i in Message.objects.all():
            i.delete()

    def send_message(self, body, number_to, number_from = None):
        if number_from is None:
            number_from = self.default_number
        message = self.client.messages \
            .create(
            body=body,
            from_=number_from,
            to=number_to
        )

    def save_messages(self, request, is_patient, real_request = True):
        if real_request:
            pull = lambda x : request.POST.get(x)
        else:
            pull = lambda x: request.get(x)
        body = pull("Body")
        phone_number = pull("From")

        print()
        print(body, phone_number)
        print()

        patient = Patient.objects.filter(phone_number = phone_number)[0]
        message = Message(patient = patient, message = body, is_patient = is_patient)
        message.save()

    def send_questions(self, patient):
        messages = Message.objects.filter(patient = patient)
        messages = [i.message for i in messages if not i.is_patient]
        print(messages)
        for i in self.questions:
            if i not in messages:
                print(i)
                self.send_message(i, str(patient.phone_number))
                self.save_messages({"Body": i, "From": str(patient.phone_number)}, is_patient=False, real_request=False)
                return
        return



if __name__ == "__main__":
    inter = SeRe()
    inter.send_message("message content", '+15191234123')
