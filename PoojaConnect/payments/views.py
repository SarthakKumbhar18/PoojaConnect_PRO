from decimal import Decimal
from tkinter import Canvas
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from bookings.models import Appointment
from .models import Payment

from django.contrib import messages
from .models import Invoice

from decimal import Decimal
from django.http import HttpResponse
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas  


from django.conf import settings
import razorpay

from django.utils import timezone


from notifications.utils import notify
from django.utils import timezone
# Create your views here.

@login_required
def create_invoice(request, appointment_id):
    appointment  = get_object_or_404(Appointment, id = appointment_id)

    if appointment.status != 'Confirmed':
        messages.error(request, "Appointment not confirmed.")
        return redirect('pandit_dashboard')
    
    if hasattr(appointment, 'invoice'):
        messages.warning(request, "Invoice already created")
        return redirect('pandit_dashboard')
    
    if request.method == 'POST':
        base_fee = Decimal(request.POST.get('base_fee', 0))
        pooja_samagri_fee = Decimal(request.POST.get('material_fee', 0))
        miscellaneous_fee = Decimal(request.POST.get('travel_fee', 0))

        total_amount = base_fee + pooja_samagri_fee + miscellaneous_fee

        Invoice.objects.create(
            appointment = appointment,
            base_fee = base_fee,
            pooja_samagri_fee = pooja_samagri_fee,
            miscellaneous_fee = miscellaneous_fee,
            total_amount = total_amount
        )

        messages.success(request, "Invoice created successfully.")

        notify(
        user=appointment.user,
        title="Invoice Generated",
        message=f"An invoice has been generated for your appointment. Please complete the payment.",
        link="/users/dashboard/",
        send_email=True
        )
        
        return redirect('pandit_dashboard')
    
    return render(request, 'payments/create_invoice.html',{'appointment' : appointment})



@login_required
def  make_payment(request, invoice_id):
    invoice = get_object_or_404(Invoice, id=invoice_id)
    print(invoice)

    amount_paise = int(invoice.total_amount * 100)
    client = razorpay.Client(
    auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))

    razorpay_order = client.order.create({"amount": amount_paise,"currency": "INR","payment_capture": 1})

    appointment = invoice.appointment
    invoice = invoice
    user = invoice.appointment.user
    pandit = invoice.appointment.pandit.user
    razorpay_order_id = razorpay_order['id']
    amount = invoice.total_amount

    payment, created = Payment.objects.get_or_create(
    appointment=appointment,
    defaults={'invoice': invoice,'user': user,'pandit': pandit,'razorpay_order_id': razorpay_order_id,'amount': amount,'status': 'Pending'})


    return render(request, 'payments/pay_invoice.html',{"invoice" : invoice, "payment" : payment, "razorpay_key" : settings.RAZORPAY_KEY_ID, "order_id" : razorpay_order['id'], "amount" : amount_paise})





def invoice_pdf(request, invoice_id):
    invoice = get_object_or_404(Invoice, id=invoice_id)
    appointment = invoice.appointment
    pandit_user = appointment.pandit.user
    user = appointment.user

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="invoice_{invoice.id}.pdf"'

    p = canvas.Canvas(response, pagesize=A4)
    width, height = A4

    y = height - 40

    
    p.setFont("Helvetica-Bold", 18)
    p.drawCentredString(width / 2, y, "PoojaConnect Invoice")

    y -= 30
    p.setFont("Helvetica", 10)
    p.drawString(40, y, f"Invoice ID: {invoice.id}")
    p.drawRightString(width - 40, y, f"Date: {invoice.created_at.strftime('%d-%m-%Y')}")

    y -= 25
    p.line(40, y, width - 40, y)


    y -= 25
    p.setFont("Helvetica-Bold", 11)
    p.drawString(40, y, "Billed By:")
    p.drawString(width / 2, y, "Billed To:")

    y -= 18
    p.setFont("Helvetica", 11)
    p.drawString(40, y, f"Pandit: {pandit_user.username}")
    p.drawString(width / 2, y, f"User: {user.username}")

    y -= 30

    
    p.setFont("Helvetica-Bold", 11)
    p.rect(40, y, width - 80, 25)
    p.drawString(50, y + 8, "Description")
    p.drawRightString(width - 60, y + 8, "Amount (₹)")

    
    p.setFont("Helvetica", 11)
    row_height = 25

    def draw_row(text, amount):
        nonlocal y
        y -= row_height
        p.rect(40, y, width - 80, row_height)
        p.drawString(50, y + 8, text)
        p.drawRightString(width - 60, y + 8, f"{amount}")

    draw_row("Pooja Fee", invoice.base_fee)
    draw_row("Pooja Samagri Fee", invoice.pooja_samagri_fee)
    draw_row("Miscellaneous Fee", invoice.miscellaneous_fee)

    
    y -= row_height
    p.setFont("Helvetica-Bold", 12)
    p.rect(40, y, width - 80, row_height)
    p.drawString(50, y + 8, "Total Amount")
    p.drawRightString(width - 60, y + 8, f" ₹ {invoice.total_amount}")

    
    y -= 40
    p.setFont("Helvetica", 10)
    p.drawCentredString(width / 2, y, "Thank you for using PoojaConnect")
    p.drawCentredString(width / 2, y - 15, "This is a system-generated invoice")

    p.showPage()
    p.save()

    return response




def verify_payment(request):
    payment_id = request.GET.get('payment_id')
    order_id = request.GET.get('order_id')
    signature = request.GET.get('signature')


    try :
        payment = Payment.objects.get(razorpay_order_id = order_id)

        client = razorpay.Client(auth = (settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))

        params_dict = {"razorpay_order_id" : order_id, "razorpay_payment_id" : payment_id, "razorpay_signature" : signature}

        client.utility.verify_payment_signature(params_dict)

        payment.razorpay_payment_id = payment_id
        payment.razorpay_signature = signature
        payment.status = 'Paid'
        payment.paid_at = timezone.now()
        payment.save()

        appointment = payment.appointment
        user = appointment.user
        pandit_user = appointment.pandit.user
        amount = payment.amount

        notify(
            user=user,
            title="Payment Successful",
            message=f"Your payment of ₹{amount} has been received successfully.",
            link="/users/dashboard/",
            send_email=True
        )

        notify(
            user=pandit_user,
            title="Payment Received",
            message=f"You received ₹{amount} for an appointment with {user.username}.",
            link="/pandits/dashboard/",
            send_email=True
        )

        return redirect('payment_success')
    
    except Exception as e:
        try:
            payment.status = 'Failed'
            payment.save()

            notify(
                user=payment.user,
                title="Payment Failed",
                message="Your payment attempt failed. Please try again.",
                link="/users/dashboard/",
                send_email=True
                )
        except:
            pass
    

        return redirect('payment_failed')
    

def payment_success(request):
    return render(request, 'payments/success.html')

def payment_failed(request):
    return render(request, 'payments/failed.html')


@login_required
def user_payment_history(request):
    payments = Payment.objects.filter(user = request.user).order_by("-created_at")

    return render(request, 'payments/user_payment_history.html', {'payments' : payments})

@login_required
def pandit_payment_history(request):
    payments = Payment.objects.filter(pandit = request.user, status = 'paid').order_by("-created_at")

    return render(request, 'payments/pandit_payment_history.html', {'payments' : payments})