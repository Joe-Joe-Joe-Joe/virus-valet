import os
from twilio.rest import Client
from .models import (Patient, Message, UserData)
from dateutil.parser import parse

def get_prepared_string(s):
    return s.casefold().strip()

def is_yes_or_no(s):
    return get_prepared_string(s) in ['yes', 'no']

def isint(x):
    try:
        int(x)
        return True
    except:
        return False

def parse_date(s):
    try:
        #parse(s)
        s
        return True
    except ValueError:
        return False

class RecieveSend:
    def __init__(self):
        #self.full_reset()
        #self.clear_messages()

        values = open("C:\\dev\\Hackathon\\RoboHacks\\virus-valet\\secrets.hidden", "r").read().split()
        self.sid = values[0]
        self.token = values[1]
        self.client = Client(self.sid, self.token)
        self.default_number = "+12262708145"
        self.questions = {
            "What is your address? This is to establish your identity." :
                lambda answer, patient: get_prepared_string(answer) == get_prepared_string(patient.address),
            "What is your date of birth?" :
                lambda answer, patient: get_prepared_string(answer) == get_prepared_string(str(patient.date_of_birth))
            ,
            "Have you experienced any cold or flu-like symptoms in the past 14 days?":
                lambda answer, patient: is_yes_or_no(answer),
            "Where could you have acquired your infection from in the past 14 days?":
                lambda answer, patient: True,
            "Do you attend a school or a workplace?":
                lambda answer, patient: is_yes_or_no(answer),
            "Yes, What is your school or workplace's name?":
                lambda answer, patient: True,
            "Have you started self-isolating?":
                lambda answer, patient: is_yes_or_no(answer),
            "When did you start self-isolating?":
                lambda answer, patient: parse_date(answer),
        }
        self.symptom_questions = {
            'How old are you?' : lambda x, y : isint(x),
            'Have you been experiencing a dry cough?': lambda x, y : is_yes_or_no(x),
            'Have you been experiencing a sore throat': lambda x, y : is_yes_or_no(x),
            'Have you been experiencing sudden or unexpected weakness?' : lambda x, y : is_yes_or_no(x),
            'Have you been experiencing a breathing problem?' : lambda x, y : is_yes_or_no(x),
            'Have you been experiencing drowsiness?' : lambda x, y : is_yes_or_no(x),
            'Have you been experiencing a pain in your chest?' : lambda x, y : is_yes_or_no(x),
            'Have you traveled to infected countries recently?' : lambda x, y : is_yes_or_no(x),
            'Do you have diabetes?': lambda x, y : is_yes_or_no(x),
            'Do you have heart disease?' : lambda x, y : is_yes_or_no(x),
            'Do you have lung disease?': lambda x, y : is_yes_or_no(x),
            'Have you had a stroke or do you have reduced immunity?': lambda x, y : is_yes_or_no(x),
            'Have your symptoms gotten worse in the past few days?': lambda x, y : is_yes_or_no(x),
            'Do you have high blood pressure?': lambda x, y : is_yes_or_no(x),
            'Do you have kidney disease?': lambda x, y : is_yes_or_no(x),
            'Have you recently had a sudden change in appetite?': lambda x, y : is_yes_or_no(x),
            'Do you had a loss of sense of smell?': lambda x, y : is_yes_or_no(x),
        }

    def full_reset(self):
       for i in Patient.objects.all():
           i.delete()
       for i in Message.objects.all():
           i.delete()

    def clear_messages(self):
        for i in Message.objects.all():
            i.delete()
        for i in UserData.objects.all():
            i.delete()
        for i in Patient.objects.all():
            i.asked_about_symptoms = False
            i.save()



    def print_messages(self):
        for i in Message.objects.all():
            print(i, i.id)

    def send_message(self, body, number_to, number_from = None):
        if number_from is None:
            number_from = self.default_number
        message = self.client.messages \
            .create(
            body=body,
            from_=number_from,
            to=number_to
        )

    def check_answer(self, patient, body, question_set = 0):
        messages = Message.objects.filter(patient = patient)
        questions = [i for i in messages if i.is_question]
        if len(questions):
            questions.reverse()
            for current_question in questions:
                if not patient.asked_about_symptoms:
                    checking_function = self.questions.get(current_question.message)
                else:
                    checking_function = self.symptom_questions.get(current_question.message)
                if checking_function and checking_function(body, patient):
                    return current_question.id
            return -1
        return -1


    def save_messages(self, request, is_patient, is_nurse = False, is_question = False, real_request = True, data_set = 0):
        if real_request:
            pull = lambda x : request.POST.get(x)
        else:
            pull = lambda x: request.get(x)
        body = pull("Body")
        phone_number = pull("From")

        # print()
        # print("Saved:", body, phone_number)
        # print()
        try:
            patient = Patient.objects.filter(phone_number = phone_number)[0]
        except:
            pass
        messages = list(Message.objects.filter(patient = patient))
        nurse_questions = [i for i in messages if i.is_question and i.sent_by_nurse]


        answer_ids = [i.is_answer for i in Message.objects.filter(patient = patient) if i.is_answer > 0]
        is_answer = self.check_answer(patient, body, data_set) # and is_patient and not is_question
        if not is_nurse and is_answer in answer_ids:
            is_answer = -1
        if is_nurse:
            is_answer = -1
        if len(messages) and len(nurse_questions) and messages[-1].id == nurse_questions[-1].id:
            is_answer = nurse_questions[-1].id
        message = Message(patient = patient, message = body, is_patient = is_patient, is_question = is_question, is_answer = is_answer, sent_by_nurse = is_nurse)
        message.save()
        questions = [i.message for i in messages if i.is_question]
        if is_answer > 0 and len(questions) and questions[-1] == list(self.questions.keys())[-1]:
            print("last question ask for the symptoms maybe")
            #self.ask_symptoms(patient, is_answer)
        return is_answer

    def ask_symptoms(self, patient, is_answer = 1):
        #if they have symptoms

        print('mother fucker')
        patient.asked_about_symptoms = True
        patient.save()
        data = self.gather_user_data(patient)
        if not data.is_symptomatic:
            return
        print("sympomatic")
        #else ask
        messages = Message.objects.filter(patient=patient)
        bot_questions = [i.message for i in messages if i.is_question and not i.sent_by_nurse and i.message not in self.questions.keys()]
        nurse_questions = [i.message for i in messages if i.is_question and i.sent_by_nurse]
        questions = [i.message for i in messages if i.is_question and i not in self.questions.keys()]
        if len(messages) and len(bot_questions) and is_answer < 0:
            if bot_questions[-1] != list(self.symptom_questions.keys())[-1]:
                print("shitter")
                self.send_message(f"Sorry, but that answer wasn't recognized.\n\n{bot_questions[-1]}",
                                  str(patient.phone_number))
                self.save_messages({"Body": f"Sorry, but that answer wasn't recognized.\n\n{questions[-1]}",
                                    "From": str(patient.phone_number)}, is_patient=False, real_request=False, data_set=1)
                return
            else:
                print("done")
                return
        question_ids = [i.id for i in messages if i.is_question]
        answer_ids = [i.is_answer for i in messages if i.is_answer > 0]
        for i in self.symptom_questions:
            if i not in questions:
                self.send_message(i, str(patient.phone_number))
                self.save_messages({"Body": i, "From": str(patient.phone_number)}, is_patient=False, is_question=True,
                                   real_request=False, data_set=1)
                return
        return


    def send_questions(self, patient, is_answer = 1):
        if patient.asked_about_symptoms:
            self.ask_symptoms(patient, is_answer)
            return
        messages = Message.objects.filter(patient = patient)
        bot_questions = [i.message for i in messages if i.is_question and not i.sent_by_nurse]
        # if len(bot_questions) and bot_questions[-1] in self.symptom_questions.keys() and bot_questions[-1] != list(self.symptom_questions.keys())[-1]:
        #     self.ask_symptoms(patient, is_answer)
        #     return
        nurse_questions = [i.message for i in messages if i.is_question and i.sent_by_nurse]
        questions = [i.message for i in messages if i.is_question]
        if len(messages) and len(bot_questions) and is_answer < 0:
            if bot_questions[-1] != list(self.questions.keys())[-1]:
                self.send_message(f"Sorry, but that answer wasn't recognized.\n\n{bot_questions[-1]}", str(patient.phone_number))
                self.save_messages({"Body": f"Sorry, but that answer wasn't recognized.\n\n{questions[-1]}", "From": str(patient.phone_number)}, is_patient=False, real_request=False)
                return
            else:
                self.ask_symptoms(patient, is_answer)
                return

        question_ids = [i.id for i in messages if i.is_question]
        answer_ids = [i.is_answer for i in messages if i.is_answer > 0]
        if len(question_ids) != len(answer_ids):
            self.ask_symptoms(patient, is_answer)
            return
        for i in self.questions:
            if i not in questions:
                self.send_message(i, str(patient.phone_number))
                self.save_messages({"Body": i, "From": str(patient.phone_number)}, is_patient=False, is_question=True, real_request=False)
                return
        return

    def gather_user_data(self, patient):
        data = UserData.objects.filter(patient = patient)
        if len(data) and False:
            return data[0]
        else:
            messages = Message.objects.filter(patient = patient)
            if not len(messages):
                data = UserData(patient=patient)
                data.save()
                return data
            question_answers = {Message.objects.get(id = i.is_answer).message: i.message for i in messages if i.is_answer > 0}
            def find_responses_related(x, check_list):
                try:
                    values = [question_answers.get(i) for i in question_answers if x in i][0].lower()
                    return values in check_list
                except:
                    return False

            is_symptomatic = find_responses_related("symptoms in the past 14 days", ['yes', 'y'])
            attending_public = find_responses_related("Where could you have acquired your infection in", ['yes', 'y'])
            not_isolating = find_responses_related("Have you started self-isolating", ["n", "no"])
            data = UserData(patient = patient, is_symptomatic = True, attending_public = attending_public, not_isolating = not_isolating) #FIX THIS LINE FIX THIS LINE FIX THIS LINE
            data.save()
            return data

    def yes_check(self, x):
        if x in ['yes', 'y']:
            return 1
        return 0

    def gather_user_symptoms(self, patient):
        try:
            data = self.gather_user_data(patient)
            if not data.is_symptomatic:
                return -1
            messages = Message.objects.filter(patient = patient)
            answers = [i for i in messages if i.is_answer > 0]
            questions_answers = [i.message for i in answers if Message.objects.get(id = i.is_answer).message in self.symptom_questions]

            def find_responses_related(x, check_list):
                try:
                    values = [question_answers.get(i) for i in question_answers if x in i][0].lower()
                    return values in check_list
                except:
                    return False
            data = [int(questions_answers[0])] + [self.yes_check(i) for i in questions_answers[1:]]
            return data
        except:
            return -1







