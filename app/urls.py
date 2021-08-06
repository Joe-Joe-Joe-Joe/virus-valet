from django.urls import path

from .views import (
    nurse_dashboard_view,
    patient_detail_view,
    sms_view,
    patient_form_view,
    add_new_message_form_view
)

urlpatterns = [
    path('', nurse_dashboard_view, name='nurse_dashboard_url'),
    path('sms/', sms_view, name = 'sms_url'),
    path('dashboard/', nurse_dashboard_view, name='nurse_dashboard_url'),
    path('patient/<int:patient_id>/', patient_detail_view, name='patient_detail_url'),
    path('patient/', patient_form_view, name='patient_form_url'),
    path('send/<int:patient_id>/', add_new_message_form_view, name='add_new_message_form_url')
]
