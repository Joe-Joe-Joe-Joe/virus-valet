from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import (
    render,
    redirect,
    reverse,
)
from django.contrib import messages

from .twilio_handler import RecieveSend

from .forms import (
    PatientForm,
    AddMessageForm
)

from .models import (
    Patient,
    Message
)

inter = RecieveSend()


#automated message functions
def greeting(patient):
    return f'You are being contacted by the Local Health Unit to monitor your COVID-19 symptoms. \n\n' \
    f'Our records show your full legal name as {patient.first_name} {patient.last_name} and your date of birth as ' \
    f'{patient.date_of_birth}.\n\n If any of this information is inaccurate, text "INFO". \n\nOtherwise, text "NEXT". ' \
    f'If at any time you wish to speak with a service representative, call 1-111-1-HEALTH.'



def nurse_dashboard_view(request):
    context = {}
    context["patients"] = Patient.objects.all()
    context["test"] = "hello world"
    return render(request, "nurse_dashboard_template.html", context)

def patient_detail_view(request, patient_id):
    patient = Patient.objects.get(id=patient_id)
    context = {"patient": patient}
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
            messages.add_message(request, messages.ERROR, 'Format Phone Numbers like +41524204242')

    form = PatientForm()
    context = {}
    context['form'] = form
    return render(request, "patient_form_template.html", context)
  
def add_new_message_form_view(request, patient_id):
    patient = Patient.objects.get(id = patient_id)
    if request.method == 'POST':
        form = AddMessageForm(request.POST)
        if form.is_valid():
            message = Message(
                patient = patient,
                message = form.cleaned_data.get('message'),
                is_patient = False,
                sent_by_nurse = True,
            )

            inter.send_message(message.message, message.patient.phone_number.as_e164)
            inter.save_messages({"Body": message.message, "From" : str(message.patient.phone_number)}, is_patient=False, is_nurse=True, is_question=False, real_request=False)
            messages.add_message(request, messages.SUCCESS, 'Message sent')
        else:
            messages.add_message(request, messages.ERROR, 'Please Try Again')
    form = AddMessageForm()
    context = {'form': form, "patient": patient}
    return render(request, "add_new_message_form_template.html", context)
