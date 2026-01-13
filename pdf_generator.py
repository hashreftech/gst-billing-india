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
from utils import get_state_name, number_to_words
from currency_utils import format_rupee

# Set this to True to use 'Rs.' instead of '₹' symbol if fonts don't display properly
USE_FALLBACK_CURRENCY = False

# Register DejaVu fonts for proper rupee symbol display
try:
    # Register the regular font
    pdfmetrics.registerFont(TTFont('DejaVuSans', 'static/fonts/DejaVuSans.ttf'))
    
    # Register the bold font
    pdfmetrics.registerFont(TTFont('DejaVuSans-Bold', 'static/fonts/DejaVuSans-Bold.ttf'))
    
    # Register font family to properly handle bold text
    pdfmetrics.registerFontFamily('DejaVuSans', normal='DejaVuSans', bold='DejaVuSans-Bold')
    
    print("Successfully loaded DejaVu fonts for PDF generation")
except Exception as e:
    print(f"Error loading fonts: {e}")
    # Set to use fallback currency format
    USE_FALLBACK_CURRENCY = True

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
    
    # Determine which fonts to use based on availability
    normal_font = 'DejaVuSans' if not USE_FALLBACK_CURRENCY else 'Helvetica'
    bold_font = 'DejaVuSans-Bold' if not USE_FALLBACK_CURRENCY else 'Helvetica-Bold'
    
    # Update styles to use the registered font
    styles['Normal'].fontName = normal_font
    styles['Normal'].fontSize = 10
    styles['Heading1'].fontName = bold_font
    styles['Heading2'].fontName = bold_font
    styles['Heading3'].fontName = bold_font
    
    # Custom styles
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        spaceAfter=20,
        alignment=TA_CENTER,
        textColor=colors.darkblue,
        fontName=bold_font
    )
    
    header_style = ParagraphStyle(
        'CustomHeader',
        parent=styles['Heading2'],
        fontSize=14,
        spaceAfter=10,
        textColor=colors.darkblue,
        fontName=bold_font
    )
    
    normal_style = ParagraphStyle(
        'CustomNormal',
        parent=styles['Normal'],
        fontSize=10,
        spaceAfter=6,
        fontName=normal_font
    )
    
    # Update styles to use the registered font
    styles['Normal'].fontName = 'DejaVuSans'
    styles['Normal'].fontSize = 10
    
    # Ensure all custom styles also use the new font
    title_style.fontName = 'DejaVuSans'
    header_style.fontName = 'DejaVuSans'
    normal_style.fontName = 'DejaVuSans'
    
    # Add company logo if available
    if company.logo_path:
        logo_path = os.path.join('uploads', company.logo_path)
        if os.path.exists(logo_path):
            try:
                # Create logo image with reasonable size
                logo = Image(logo_path, width=2*inch, height=1*inch, kind='proportional')
                logo.hAlign = 'CENTER'
                story.append(logo)
                story.append(Spacer(1, 10))
            except Exception as e:
                print(f"Error loading logo: {e}")
    
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
        ('FONTNAME', (0, 0), (-1, -1), normal_font),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('LEFTPADDING', (0, 0), (-1, -1), 0),
        ('RIGHTPADDING', (0, 0), (-1, -1), 0),
        ('TOPPADDING', (0, 0), (-1, -1), 2),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 2),
    ]))
    
    story.append(invoice_details_table)
    story.append(Spacer(1, 20))
    
    # Create a special Paragraph style for currency values
    amount_style = ParagraphStyle(
        'AmountStyle',
        parent=normal_style,
        fontName=normal_font,
        alignment=TA_RIGHT
    )
    
    # Items table header
    items_data = [
        ['S.No', 'Description', 'HSN', 'Qty', 'Unit', 'Rate', 'Amount', 'CGST%', 'SGST%', 'GST Amt', 'Total']
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
            Paragraph(format_rupee(item.rate, True, USE_FALLBACK_CURRENCY), amount_style),
            Paragraph(format_rupee(item.amount, True, USE_FALLBACK_CURRENCY), amount_style),
            f"{item.cgst_rate:.1f}%" if hasattr(item, 'cgst_rate') and item.cgst_rate else f"{item.gst_rate/2:.1f}%",
            f"{item.sgst_rate:.1f}%" if hasattr(item, 'sgst_rate') and item.sgst_rate else f"{item.gst_rate/2:.1f}%",
            Paragraph(format_rupee(gst_amount, True, USE_FALLBACK_CURRENCY), amount_style),
            Paragraph(format_rupee(total_amount, True, USE_FALLBACK_CURRENCY), amount_style)
        ])
    
    # Items table
    items_table = Table(items_data, colWidths=[
        0.4*inch, 2.0*inch, 0.5*inch, 0.5*inch, 0.5*inch, 
        0.7*inch, 0.7*inch, 0.5*inch, 0.5*inch, 0.7*inch, 0.8*inch
    ])
    
    items_table.setStyle(TableStyle([
        # Header styling
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), bold_font),
        ('FONTSIZE', (0, 0), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        
        # Data styling
        ('ALIGN', (1, 1), (1, -1), 'LEFT'),  # Description left aligned
        ('ALIGN', (2, 1), (-1, -1), 'RIGHT'),  # Numbers right aligned
        ('FONTNAME', (0, 1), (-1, -1), normal_font),
        ('FONTSIZE', (0, 1), (-1, -1), 8),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))
    
    story.append(items_table)
    story.append(Spacer(1, 20))
    
    # Totals table
    # Use Paragraph objects with our special style for currency values
    # This gives better control over the font used for rendering the rupee symbol
    totals_data = [
        ['', 'Subtotal:', Paragraph(format_rupee(bill.subtotal, True, USE_FALLBACK_CURRENCY), amount_style)],
    ]
    
    # Add discount if present
    if hasattr(bill, 'discount_amount') and bill.discount_amount and float(bill.discount_amount) > 0:
        discount_label = "Discount"
        if hasattr(bill, 'discount_type') and bill.discount_type == 'percentage' and hasattr(bill, 'discount_value'):
            discount_label += f" ({float(bill.discount_value):.1f}%)"
        discount_label += ":"
        discount_value = f"-{format_rupee(float(bill.discount_amount), True, USE_FALLBACK_CURRENCY)}"
        totals_data.append(['', discount_label, Paragraph(discount_value, amount_style)])
    
    if bill.cgst_amount > 0:
        totals_data.append(['', 'CGST:', Paragraph(format_rupee(bill.cgst_amount, True, USE_FALLBACK_CURRENCY), amount_style)])
    if bill.sgst_amount > 0:
        totals_data.append(['', 'SGST:', Paragraph(format_rupee(bill.sgst_amount, True, USE_FALLBACK_CURRENCY), amount_style)])
    if bill.igst_amount > 0:
        totals_data.append(['', 'IGST:', Paragraph(format_rupee(bill.igst_amount, True, USE_FALLBACK_CURRENCY), amount_style)])
    
    totals_data.append(['', 'Total Amount:', Paragraph(format_rupee(bill.total_amount, True, USE_FALLBACK_CURRENCY), amount_style)])
    
    totals_table = Table(totals_data, colWidths=[4*inch, 1.5*inch, 1.5*inch])
    totals_table.setStyle(TableStyle([
        ('ALIGN', (1, 0), (-1, -1), 'RIGHT'),
        ('FONTNAME', (1, -1), (-1, -1), bold_font),
        ('FONTNAME', (0, 0), (1, -2), normal_font),
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
