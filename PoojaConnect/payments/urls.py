from django.urls import path
from .views import *

urlpatterns = [
    path('pay/<int:invoice_id>/', make_payment, name='make_payment'),
    path('invoice/create/<int:appointment_id>/', create_invoice, name = 'create_invoice'),
    path('invoice/pdf/<int:invoice_id>/', invoice_pdf, name='invoice_pdf'),
    path('user/history/', user_payment_history, name='user_payment_history'),
    path('pandit/history/', pandit_payment_history, name='pandit_payment_history'),
]