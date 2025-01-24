def format_kes(amount):
    """Format amount in Kenyan Shillings (in thousands)"""
    if abs(amount) >= 1000:
        # For amounts >= 1M (after scaling), show in millions
        return f"KES {amount/1000:,.1f}M"
    else:
        # For amounts < 1M (after scaling), show in thousands
        return f"KES {amount:,.1f}K"