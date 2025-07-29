import io
import os
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image
from reportlab.lib.enums import TA_LEFT, TA_RIGHT, TA_CENTER
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from datetime import datetime
from utils import format_currency, get_state_name, number_to_words

# Register a font that supports the rupee symbol
pdfmetrics.registerFont(TTFont('DejaVuSans', 'static/fonts/DejaVuSans.ttf'))

def generate_invoice_pdf(bill, company):
    """Generate PDF invoice for a bill"""
    buffer = io.BytesIO()
    
    # Create PDF document
    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=0.5*inch,
        leftMargin=0.5*inch,
        topMargin=0.5*inch,
        bottomMargin=0.5*inch
    )
    
    # Build story (content)
    story = []
    styles = getSampleStyleSheet()
    
    # Custom styles
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        spaceAfter=20,
        alignment=TA_CENTER,
        textColor=colors.darkblue
    )
    
    header_style = ParagraphStyle(
        'CustomHeader',
        parent=styles['Heading2'],
        fontSize=14,
        spaceAfter=10,
        textColor=colors.darkblue
    )
    
    normal_style = ParagraphStyle(
        'CustomNormal',
        parent=styles['Normal'],
        fontSize=10,
        spaceAfter=6
    )
    
    # Update styles to use the registered font
    styles['Normal'].fontName = 'DejaVuSans'
    styles['Normal'].fontSize = 10
    
    # Ensure all custom styles also use the new font
    title_style.fontName = 'DejaVuSans'
    header_style.fontName = 'DejaVuSans'
    normal_style.fontName = 'DejaVuSans'
    
    # Title
    story.append(Paragraph("TAX INVOICE", title_style))
    story.append(Spacer(1, 20))
    
    # Company and customer details table
    company_customer_data = []
    
    # Company details
    company_address = company.address.replace('\n', '<br/>')
    company_details = f"""
    <b>{company.name}</b><br/>
    {company_address}<br/>
    <b>GSTIN:</b> {company.gst_number}<br/>
    <b>State:</b> {get_state_name(company.state_code)} ({company.state_code})
    """
    if company.tan_number:
        company_details += f"<br/><b>TAN:</b> {company.tan_number}"
    
    # Customer details
    customer = bill.customer
    customer_details = f"""
    <b>Bill To:</b><br/>
    <b>{customer.name}</b><br/>
    """
    if customer.address:
        customer_address = customer.address.replace('\n', '<br/>')
        customer_details += f"{customer_address}<br/>"
    if customer.gst_number:
        customer_details += f"<b>GSTIN:</b> {customer.gst_number}<br/>"
    if customer.state_code:
        customer_details += f"<b>State:</b> {get_state_name(customer.state_code)} ({customer.state_code})<br/>"
    if customer.phone:
        customer_details += f"<b>Phone:</b> {customer.phone}<br/>"
    if customer.email:
        customer_details += f"<b>Email:</b> {customer.email}"
    
    company_customer_data = [
        [Paragraph(company_details, normal_style), Paragraph(customer_details, normal_style)]
    ]
    
    company_customer_table = Table(company_customer_data, colWidths=[3.5*inch, 3.5*inch])
    company_customer_table.setStyle(TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('LEFTPADDING', (0, 0), (-1, -1), 0),
        ('RIGHTPADDING', (0, 0), (-1, -1), 0),
    ]))
    
    story.append(company_customer_table)
    story.append(Spacer(1, 20))
    
    # Invoice details
    invoice_details_data = [
        ['Invoice No:', bill.bill_number, 'Invoice Date:', bill.bill_date.strftime('%d/%m/%Y')],
    ]
    if bill.due_date:
        invoice_details_data.append(['Due Date:', bill.due_date.strftime('%d/%m/%Y'), '', ''])
    
    invoice_details_table = Table(invoice_details_data, colWidths=[1.2*inch, 1.8*inch, 1.2*inch, 1.8*inch])
    invoice_details_table.setStyle(TableStyle([
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('LEFTPADDING', (0, 0), (-1, -1), 0),
        ('RIGHTPADDING', (0, 0), (-1, -1), 0),
        ('TOPPADDING', (0, 0), (-1, -1), 2),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 2),
    ]))
    
    story.append(invoice_details_table)
    story.append(Spacer(1, 20))
    
    # Items table header
    items_data = [
        ['S.No', 'Description', 'HSN', 'Qty', 'Unit', 'Rate', 'Amount', 'GST%', 'GST Amt', 'Total']
    ]
    
    # Items data
    for i, item in enumerate(bill.items, 1):
        gst_amount = item.cgst_amount + item.sgst_amount + item.igst_amount
        total_amount = item.amount + gst_amount
        
        items_data.append([
            str(i),
            f"{item.product_name}\n{item.description or ''}",
            item.hsn_code,
            f"{item.quantity:.2f}",
            item.unit,
            f"₹{item.rate:.2f}",
            f"₹{item.amount:.2f}",
            f"{item.gst_rate:.1f}%",
            f"₹{gst_amount:.2f}",
            f"₹{total_amount:.2f}"
        ])
    
    # Items table
    items_table = Table(items_data, colWidths=[
        0.4*inch, 2.2*inch, 0.6*inch, 0.5*inch, 0.5*inch, 
        0.8*inch, 0.8*inch, 0.5*inch, 0.8*inch, 0.9*inch
    ])
    
    items_table.setStyle(TableStyle([
        # Header styling
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        
        # Data styling
        ('ALIGN', (1, 1), (1, -1), 'LEFT'),  # Description left aligned
        ('ALIGN', (2, 1), (-1, -1), 'RIGHT'),  # Numbers right aligned
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 8),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))
    
    story.append(items_table)
    story.append(Spacer(1, 20))
    
    # Totals table
    totals_data = [
        ['', 'Subtotal:', f"₹{bill.subtotal:.2f}"],
    ]
    
    # Add discount if present
    if hasattr(bill, 'discount_amount') and bill.discount_amount and float(bill.discount_amount) > 0:
        discount_label = "Discount"
        if hasattr(bill, 'discount_type') and bill.discount_type == 'percentage' and hasattr(bill, 'discount_value'):
            discount_label += f" ({float(bill.discount_value):.1f}%)"
        discount_label += ":"
        totals_data.append(['', discount_label, f"-₹{float(bill.discount_amount):.2f}"])
    
    if bill.cgst_amount > 0:
        totals_data.append(['', 'CGST:', f"₹{bill.cgst_amount:.2f}"])
    if bill.sgst_amount > 0:
        totals_data.append(['', 'SGST:', f"₹{bill.sgst_amount:.2f}"])
    if bill.igst_amount > 0:
        totals_data.append(['', 'IGST:', f"₹{bill.igst_amount:.2f}"])
    
    totals_data.append(['', 'Total Amount:', f"₹{bill.total_amount:.2f}"])
    
    totals_table = Table(totals_data, colWidths=[4*inch, 1.5*inch, 1.5*inch])
    totals_table.setStyle(TableStyle([
        ('ALIGN', (1, 0), (-1, -1), 'RIGHT'),
        ('FONTNAME', (1, -1), (-1, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('LINEBELOW', (1, -1), (-1, -1), 2, colors.black),
    ]))
    
    story.append(totals_table)
    story.append(Spacer(1, 20))
    
    # Amount in words
    amount_words = f"Amount in words: {number_to_words(float(bill.total_amount))} Rupees Only"
    story.append(Paragraph(amount_words, normal_style))
    story.append(Spacer(1, 20))
    
    # Notes
    if bill.notes:
        story.append(Paragraph("<b>Notes:</b>", header_style))
        story.append(Paragraph(bill.notes, normal_style))
        story.append(Spacer(1, 20))
    
    # Footer
    footer_text = """
    <b>Terms & Conditions:</b><br/>
    1. Payment is due within 30 days of invoice date.<br/>
    2. Interest @ 2% per month will be charged on overdue amounts.<br/>
    3. All disputes subject to local jurisdiction only.
    """
    story.append(Paragraph(footer_text, normal_style))
    
    # Build PDF
    doc.build(story)
    
    # Get PDF data
    pdf_data = buffer.getvalue()
    buffer.close()
    
    # Save to temporary file and return path
    temp_filename = f"temp_invoice_{bill.bill_number}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
    temp_path = os.path.join('/tmp', temp_filename)
    
    with open(temp_path, 'wb') as f:
        f.write(pdf_data)
    
    return temp_path
