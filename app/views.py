from django.shortcuts import (
    render,
    redirect,
    reverse,
)

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

def patient_form_view(request):
    if request.method == 'POST':
        form = PatientForm(request.POST)
        if form.is_valid():
            form.save()
            print("patient created")
            return redirect(reverse('nurse_dashboard_url'))
        else:
            print("invalid patient data please try again")

    form = PatientForm()
    context = {}
    context['form'] = form
    return render(request, "patient_form_template.html", context)
