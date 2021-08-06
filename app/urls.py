from django.urls import path

from .views import (
    nurse_dashboard_view,
    patient_detail_view,
    sms_view
)

urlpatterns = [
    path('/', nurse_dashboard_view, name='nurse_dashboard_url'),
    path('sms/', sms_view, name = 'sms_url'),
    path('dashboard/', nurse_dashboard_view, name='nurse_dashboard_url'),
    path('patient/<int:patient_id>/', patient_detail_view, name='nurse_dashboard_url'),
]
