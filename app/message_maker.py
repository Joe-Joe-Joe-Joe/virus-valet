from .models import (Patient, Message)
from .twilio_handler import RecieveSend

def greeting(Patient):
    f'You are being contacted by the Local Health Unit to monitor your COVID-19 symptoms. ' \
    f'Our records show your full legal name as {self.patient.first_name} {self.patient.last_name} and your date of birth as ' \
    f'{self.patient.date_of_birth}. If any of this information is inaccurate, text "INFO". Otherwise, text "NEXT". ' \
    f'If at any time you wish to speak with a service representative, call 1-111-1-HEALTH.'

if __name__ == "__main__":
    inter = RecieveSend()
    print(Patient.objects.filter(id = 0)[0])
    #inter.send_message(greeting())