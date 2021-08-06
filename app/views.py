from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import (
    render,
    redirect,
    reverse,
)
from django.contrib import messages

from .forms import PatientForm

from .models import Patient

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
    resp = MessagingResponse()
    print(request.POST.body)
    resp.message("testing things")
    return HttpResponse(resp.to_xml(), content_type='text/xml')
    #return render(request, "sms_template.html")
    
def patient_form_view(request):
    if request.method == 'POST':
        form = PatientForm(request.POST)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, 'Patient Created')
            return redirect(reverse('nurse_dashboard_url'))
        else:
            messages.add_message(request, messages.ERROR, 'Format Phone Numbers like +41524204242')

    form = PatientForm()
    context = {}
    context['form'] = form
    return render(request, "patient_form_template.html", context)
