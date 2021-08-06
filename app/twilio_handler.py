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

    def check_answer(self, patient, body):
        messages = Message.objects.filter(patient = patient)
        questions = [i for i in messages if i.is_question]
        if len(questions):
            questions.reverse()
            for current_question in questions:
                possible_question_answers = self.questions.get(current_question.message)
                if body.lower() in possible_question_answers:
                    return current_question.id
            return -1
        return -1


    def save_messages(self, request, is_patient, is_question = False, sent_by_nurse = False, real_request = True):
        if real_request:
            pull = lambda x : request.POST.get(x)
        else:
            pull = lambda x: request.get(x)
        body = pull("Body")
        phone_number = pull("From")

        print()
        print("Saved:", body, phone_number)
        print()

        patient = Patient.objects.filter(phone_number = phone_number)[0]

        answer_ids = [i.is_answer for i in Message.objects.filter(patient = patient) if i.is_answer > 0]
        is_answer = self.check_answer(patient, body) # and is_patient and not is_question
        if is_answer in answer_ids:
            is_answer = -1
        message = Message(patient = patient, message = body, is_patient = is_patient, is_question = is_question, is_answer = is_answer, sent_by_nurse = sent_by_nurse)
        message.save()


    def send_questions(self, patient):
        messages = Message.objects.filter(patient = patient)
        questions = [i.message for i in messages if i.is_question]

        question_ids = [i.id for i in messages if i.is_question]
        answer_ids = [i.is_answer for i in messages if i.is_answer > 0]
        if len(question_ids) != len(answer_ids):
            return
        for i in self.questions:
            if i not in questions:
                self.send_message(i, str(patient.phone_number))
                self.save_messages({"Body": i, "From": str(patient.phone_number)}, is_patient=False, is_question=True, real_request=False)
                return
        return


