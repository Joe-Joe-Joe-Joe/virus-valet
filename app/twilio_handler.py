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

    def print_messages(self):
        print(Message.objects.all())

    def send_message(self, body, number_to, number_from = None):
        if number_from is None:
            number_from = self.default_number
        message = self.client.messages \
            .create(
            body=body,
            from_=number_from,
            to=number_to
        )

    def save_messages(self, request, is_patient, is_question = False, real_request = True):
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
        message = Message(patient = patient, message = body, is_patient = is_patient, is_question = is_question)
        message.save()

    def check_message_answer(self, request):
        pass

    def send_questions(self, patient):
        self.print_messages()
        messages = Message.objects.filter(patient = patient)
        messages = [i.message for i in messages if i.is_question]
        for i in self.questions:
            if i not in messages:
                self.send_message(i, str(patient.phone_number))
                self.save_messages({"Body": i, "From": str(patient.phone_number)}, is_patient=False, is_question=True, real_request=False)
                return
        return


