from django.shortcuts import render

def nurse_dashboard_view(request):
    return render(request, "nurse_dashboard_template.html")

def patient_detail_view(request, patient_id):
    context = {"patient_id": patient_id}
    return render(request, "patient_details_template.html", context)
