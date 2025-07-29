from decimal import Decimal, ROUND_HALF_UP

def calculate_gst(amount, gst_rate, seller_state, buyer_state):
    """
    Calculate GST amounts based on seller and buyer states
    
    Args:
        amount: Base amount (without tax)
        gst_rate: GST rate as percentage
        seller_state: Seller's state code
        buyer_state: Buyer's state code
    
    Returns:
        dict: {'cgst': amount, 'sgst': amount, 'igst': amount}
    """
    amount = Decimal(str(amount))
    gst_rate = Decimal(str(gst_rate))
    
    # Convert percentage to decimal
    gst_decimal = gst_rate / 100
    
    # Calculate total GST amount
    total_gst = amount * gst_decimal
    
    # Round to 2 decimal places
    total_gst = total_gst.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
    
    if seller_state == buyer_state:
        # Intra-state transaction: CGST + SGST
        cgst = (total_gst / 2).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
        sgst = (total_gst / 2).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
        igst = Decimal('0.00')
        
        # Adjust for rounding differences
        if cgst + sgst != total_gst:
            difference = total_gst - (cgst + sgst)
            cgst += difference
    else:
        # Inter-state transaction: IGST
        cgst = Decimal('0.00')
        sgst = Decimal('0.00')
        igst = total_gst
    
    return {
        'cgst': cgst,
        'sgst': sgst,
        'igst': igst
    }

def calculate_item_total(quantity, rate, gst_rate, seller_state, buyer_state):
    """
    Calculate total for a single item including GST
    
    Returns:
        dict: Complete calculation breakdown
    """
    quantity = Decimal(str(quantity))
    rate = Decimal(str(rate))
    
    # Base amount
    base_amount = quantity * rate
    base_amount = base_amount.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
    
    # GST calculation
    gst_amounts = calculate_gst(base_amount, gst_rate, seller_state, buyer_state)
    
    # Total amount
    total_gst = Decimal(str(gst_amounts['cgst'])) + Decimal(str(gst_amounts['sgst'])) + Decimal(str(gst_amounts['igst']))
    total_amount = base_amount + total_gst
    
    return {
        'quantity': float(quantity),
        'rate': float(rate),
        'base_amount': float(base_amount),
        'cgst': gst_amounts['cgst'],
        'sgst': gst_amounts['sgst'],
        'igst': gst_amounts['igst'],
        'total_gst': float(total_gst),
        'total_amount': float(total_amount)
    }

def get_gst_summary(items):
    """
    Calculate GST summary for multiple items
    
    Args:
        items: List of items with gst calculations
    
    Returns:
        dict: Summary with totals by GST rate
    """
    summary = {}
    
    for item in items:
        gst_rate = item.get('gst_rate', 0)
        
        if gst_rate not in summary:
            summary[gst_rate] = {
                'base_amount': 0,
                'cgst': 0,
                'sgst': 0,
                'igst': 0,
                'total_gst': 0,
                'total_amount': 0
            }
        
        summary[gst_rate]['base_amount'] += item.get('base_amount', 0)
        summary[gst_rate]['cgst'] += item.get('cgst', 0)
        summary[gst_rate]['sgst'] += item.get('sgst', 0)
        summary[gst_rate]['igst'] += item.get('igst', 0)
        summary[gst_rate]['total_gst'] += item.get('total_gst', 0)
        summary[gst_rate]['total_amount'] += item.get('total_amount', 0)
    
    return summary
