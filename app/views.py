from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

def nurse_dashboard_view(request):
    return render(request, "nurse_dashboard_template.html")

def patient_detail_view(request, patient_id):
    context = {"patient_id": patient_id}
    return render(request, "patient_details_template.html", context)

@csrf_exempt
def sms_view(request):
    resp = MessagingResponse()
    print(request.POST.body)
    resp.message("testing things")
    return HttpResponse(resp.to_xml(), content_type='text/xml')
    #return render(request, "sms_template.html")
