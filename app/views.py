from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import (
    render,
    redirect,
    reverse,
)
from django.contrib import messages

from django.http import HttpResponseRedirect

from .twilio_handler import RecieveSend

from .forms import (
    PatientForm,
    AddMessageForm
)

from .models import (
    Patient,
    Message
)

from time import sleep
from .deep_learning import predict

inter = RecieveSend()

img_map = {
    "red": "https://upload.wikimedia.org/wikipedia/commons/d/d5/Red_exclamation_mark.svg",
    "green": "https://upload.wikimedia.org/wikipedia/commons/b/bd/Checkmark_green.svg",
    "yellow": "https://upload.wikimedia.org/wikipedia/commons/4/4c/Traffic_cone.svg",
}


# automated message functions
def greeting(patient):
    return f'You are being contacted by the Local Health Unit to monitor your COVID-19 symptoms. \n\n' \
        f'Our records show your full legal name as {patient.first_name} {patient.last_name} and your date of birth as' \
        f' {patient.date_of_birth}.\n\n If any of this information is inaccurate, text "INFO".\n' \
        f'\nOtherwise, text "NEXT".If at any time you wish to speak with a service representative, call 1-111-1-HEALTH.'


def resend(request):
    me = Patient.objects.filter(phone_number = "+12265678330")[0]
    me.asked_about_symptoms = True
    me.save()
    inter.send_questions(patient=me)
    print("resending")
    return HttpResponse("Okay then", content_type='text/xml')

def nurse_dashboard_view(request):
    lacking_others = Patient.objects.filter(risk_to_others = -1)
    lacking_self = Patient.objects.filter(risk_to_self= -1)
    for i in lacking_others:
        data = inter.gather_user_data(i)
        if data.is_symptomatic and (data.attending_public or data.not_isolating):
            i.risk_to_others = 2
        elif data.is_symptomatic or data.attending_public or data.not_isolating:
            i.risk_to_others = 1
        else:
            i.risk_to_others = 0
        i.save()


    for i in lacking_self:
        symptoms = inter.gather_user_symptoms(i)
        print(symptoms)
        if symptoms == -1:
            i.risk_to_self = 2
        else:
            i.risk_to_self = predict(inter.gather_user_symptoms(i))
            print("SOMETHING IS HERE", predict(inter.gather_user_symptoms(i)))
        i.save()

    patients = Patient.objects.all().order_by('risk_to_self').order_by('risk_to_others').values()
    num_to_color = {
        0: "red",
        1: "yellow",
        2: "green"
    }

    for patient in patients:
        print("testing")
        patient['risk_to_selfs'] = img_map[num_to_color[patient['risk_to_self']]]
        patient['risk_to_other'] = img_map[num_to_color[patient['risk_to_others']]]

    context = {
        "patients": patients,
        "test": "hello world"
    }
    return render(request, "nurse_dashboard_template.html", context)

def patient_detail_view(request, patient_id):
    patient = Patient.objects.get(id=patient_id)
    if request.method == 'POST':
        form = AddMessageForm(request.POST)
        if form.is_valid():
            message = Message(
                patient=patient,
                message=form.cleaned_data.get('message'),
                is_patient=False,
                sent_by_nurse=True,
                is_question=True,
            )
            inter.send_message(message.message, message.patient.phone_number.as_e164)
            inter.save_messages({"Body": message.message, "From": str(message.patient.phone_number)}, is_patient=False, is_question=True, is_nurse=True, real_request=False)
            messages.add_message(request, messages.SUCCESS, 'Message sent')
        else:
            messages.add_message(request, messages.ERROR, 'Please Try Again')
        return HttpResponseRedirect(reverse('patient_detail_url', args=[patient.id]))
    raw_messages = Message.objects.filter(patient=patient).order_by('-date_created')

    patient_messages = []
    for message in raw_messages:
        name = ""
        icon=""
        if message.is_patient:
            name = "Patient"
            icon = "users"

        elif message.sent_by_nurse:
            name = "Nurse"
            icon = "medkit"

        else:
            name = "Bot"
            icon = "android"

        patient_messages.append({
            "name": name,
            "icon": icon,
            "message": message.message,
            "date": message.date_created.strftime("%Y/%m/%d %H:%M"),
        })

    context = {
        "patient": patient,
        "patient_messages": patient_messages,
    }
    return render(request, "patient_details_template.html", context)

@csrf_exempt
def sms_view(request):
    is_answer = inter.save_messages(request, True)
    patient = Patient.objects.filter(phone_number = request.POST.get("From"))[0]
    inter.send_questions(patient, is_answer)
    #inter.send_questions()
    return HttpResponse("", content_type='text/xml')
    
def patient_form_view(request):
    if request.method == 'POST':
        form = PatientForm(request.POST)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, 'Patient Created')
            phone_number = form.cleaned_data.get("phone_number")
            patient = Patient.objects.filter(phone_number = phone_number)[0]
            inter.send_message(greeting(patient), phone_number)
            inter.send_questions(patient)
            return redirect(reverse('nurse_dashboard_url'))
        else:
            messages.add_message(request, messages.ERROR, 'Format Phone Numbers like +1### ### ####')

    form = PatientForm()
    context = {}
    context['form'] = form
    return render(request, "patient_form_template.html", context)

def refresh_view(request):
    if request.method == "GET":
        num_messages = Message.objects.count()
        while True:
            if Message.objects.count() != num_messages:
                return HttpResponse("refresh")
            sleep(1)