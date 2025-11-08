import os
from django.conf import settings
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from customer.models import Payment, Invoice
import datetime

def generate_invoice_pdf(payment_id):
    """Generate PDF invoice for a payment"""
    try:
        payment = Payment.objects.get(id=payment_id)
        invoice = Invoice.objects.get(payment=payment)
        
        # Context data for template
        context = {
            'payment': payment,
            'invoice': invoice,
            'customer': payment.customer,
            'shipment': payment.shipment,
            'company': {
                'name': 'SmartRoute Logistics',
                'address': '123 Business Park, Mumbai, Maharashtra - 400001',
                'phone': '+91-9876543210',
                'email': 'accounts@smartroute.com',
                'gstin': '27AABCU9603R1ZM',
                'pan': 'AABCU9603R',
            },
            'today': datetime.date.today(),
        }
        
        template_path = 'customer/invoice_pdf.html'
        template = get_template(template_path)
        html = template.render(context)
        
        # Create PDF
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="invoice_{payment.invoice_number}.pdf"'
        
        # Generate PDF
        pisa_status = pisa.CreatePDF(html, dest=response)
        
        if pisa_status.err:
            return HttpResponse('We had some errors <pre>' + html + '</pre>')
        return response
        
    except (Payment.DoesNotExist, Invoice.DoesNotExist) as e:
        return HttpResponse(f"Error generating PDF: {str(e)}")

def generate_receipt_pdf(payment_id):
    """Generate PDF receipt for a payment"""
    try:
        payment = Payment.objects.get(id=payment_id)
        
        # Context data for template
        context = {
            'payment': payment,
            'customer': payment.customer,
            'shipment': payment.shipment,
            'company': {
                'name': 'SmartRoute Logistics',
                'address': '123 Business Park, Mumbai, Maharashtra - 400001',
                'phone': '+91-9876543210',
                'gstin': '27AABCU9603R1ZM',
            },
            'today': datetime.date.today(),
        }
        
        template_path = 'customer/receipt_pdf.html'
        template = get_template(template_path)
        html = template.render(context)
        
        # Create PDF
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="receipt_{payment.invoice_number}.pdf"'
        
        # Generate PDF
        pisa_status = pisa.CreatePDF(html, dest=response)
        
        if pisa_status.err:
            return HttpResponse('We had some errors <pre>' + html + '</pre>')
        return response
        
    except Payment.DoesNotExist as e:
        return HttpResponse(f"Error generating PDF: {str(e)}")