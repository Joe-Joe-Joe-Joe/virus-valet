from django.urls import path

from .views import (
    nurse_dashboard_view,
    patient_detail_view,
    sms_view,
    patient_form_view,
    refresh_view
)

urlpatterns = [
    path('', nurse_dashboard_view, name='nurse_dashboard_url'),
    path('sms/', sms_view, name = 'sms_url'),
    path('dashboard/', nurse_dashboard_view, name='nurse_dashboard_url'),
    path('patient/<int:patient_id>/', patient_detail_view, name='patient_detail_url'),
    path('patient/', patient_form_view, name='patient_form_url'),
    path('refresh/', refresh_view, name='refresh_url')
]
