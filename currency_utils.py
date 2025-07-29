"""
Utility functions for currency formatting and number to words conversion
with special handling for Indian rupee symbol
"""

def format_rupee(amount, space_after_symbol=True, use_fallback=False):
    """
    Format amount with rupee symbol, ensuring compatibility with PDF rendering
    
    Args:
        amount: The numeric amount to format
        space_after_symbol: Whether to include a space after the rupee symbol
        use_fallback: Whether to use 'Rs.' text instead of ₹ symbol
    
    Returns:
        Formatted string with rupee symbol and amount
    """
    if amount is None:
        amount = 0
        
    # Format the number with 2 decimal places
    formatted_amount = f"{float(amount):.2f}"
    
    # Use 'Rs.' text as a fallback if fonts have issues with ₹ symbol
    if use_fallback:
        if space_after_symbol:
            return f"Rs. {formatted_amount}"
        else:
            return f"Rs.{formatted_amount}"
    else:
        # Use rupee symbol with optional space
        if space_after_symbol:
            return f"₹ {formatted_amount}"
        else:
            return f"₹{formatted_amount}"
