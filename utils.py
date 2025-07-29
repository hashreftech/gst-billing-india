import os
from werkzeug.utils import secure_filename

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def get_state_name(state_code):
    """Get state name from state code"""
    states = {
        '01': 'Jammu and Kashmir', '02': 'Himachal Pradesh', '03': 'Punjab',
        '04': 'Chandigarh', '05': 'Uttarakhand', '06': 'Haryana',
        '07': 'Delhi', '08': 'Rajasthan', '09': 'Uttar Pradesh',
        '10': 'Bihar', '11': 'Sikkim', '12': 'Arunachal Pradesh',
        '13': 'Nagaland', '14': 'Manipur', '15': 'Mizoram',
        '16': 'Tripura', '17': 'Meghalaya', '18': 'Assam',
        '19': 'West Bengal', '20': 'Jharkhand', '21': 'Odisha',
        '22': 'Chhattisgarh', '23': 'Madhya Pradesh', '24': 'Gujarat',
        '25': 'Daman and Diu', '26': 'Dadra and Nagar Haveli',
        '27': 'Maharashtra', '28': 'Andhra Pradesh', '29': 'Karnataka',
        '30': 'Goa', '31': 'Lakshadweep', '32': 'Kerala',
        '33': 'Tamil Nadu', '34': 'Puducherry', '35': 'Andaman and Nicobar Islands',
        '36': 'Telangana', '37': 'Andhra Pradesh (New)'
    }
    return states.get(state_code, 'Unknown')

def validate_gst_number(gst_number):
    """Validate GST number format"""
    if not gst_number or len(gst_number) != 15:
        return False
    
    # GST format: 2 digits state code + 10 chars PAN + 1 char entity + 1 char checksum + 1 char 'Z' + 1 char
    import re
    pattern = r'^[0-9]{2}[A-Z]{5}[0-9]{4}[A-Z]{1}[1-9A-Z]{1}[Z]{1}[0-9A-Z]{1}$'
    return bool(re.match(pattern, gst_number))

def format_currency(amount):
    """Format currency in Indian style"""
    if amount is None:
        return "₹0.00"
    
    amount = float(amount)
    return f"₹{amount:,.2f}"

def number_to_words(amount):
    """Convert number to words (Indian format)"""
    if amount is None or amount == 0:
        return "Zero"
    
    # Convert to int for whole number processing
    amount = int(float(amount))
    
    # Number to words mapping
    ones = ["", "One", "Two", "Three", "Four", "Five", "Six", "Seven", "Eight", "Nine"]
    teens = ["Ten", "Eleven", "Twelve", "Thirteen", "Fourteen", "Fifteen", "Sixteen", "Seventeen", "Eighteen", "Nineteen"]
    tens = ["", "", "Twenty", "Thirty", "Forty", "Fifty", "Sixty", "Seventy", "Eighty", "Ninety"]
    
    def convert_hundreds(num):
        result = ""
        if num >= 100:
            result += ones[num // 100] + " Hundred "
            num %= 100
        
        if num >= 20:
            result += tens[num // 10] + " "
            num %= 10
        elif num >= 10:
            result += teens[num - 10] + " "
            num = 0
        
        if num > 0:
            result += ones[num] + " "
        
        return result.strip()
    
    if amount == 0:
        return "Zero"
    
    result = ""
    
    # Handle crores (10,000,000)
    if amount >= 10000000:
        crores = amount // 10000000
        result += convert_hundreds(crores) + " Crore "
        amount %= 10000000
    
    # Handle lakhs (100,000)
    if amount >= 100000:
        lakhs = amount // 100000
        result += convert_hundreds(lakhs) + " Lakh "
        amount %= 100000
    
    # Handle thousands
    if amount >= 1000:
        thousands = amount // 1000
        result += convert_hundreds(thousands) + " Thousand "
        amount %= 1000
    
    # Handle remaining hundreds
    if amount > 0:
        result += convert_hundreds(amount)
    
    return result.strip()
