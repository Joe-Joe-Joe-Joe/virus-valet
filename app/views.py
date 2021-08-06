from django.shortcuts import render
from .forms import PatientForm

def nurse_dashboard_view(request):
    return render(request, "nurse_dashboard_template.html")

def patient_detail_view(request, patient_id):
    context = {"patient_id": patient_id}
    return render(request, "patient_details_template.html", context)

def patient_form_view(request, patient_id):
    if request.method == 'POST':
        form = PatientForm(request.POST)
    form = PatientForm()
    context = {}
    context['form'] = form
    return render(request, "patient_form_template.html", context)
