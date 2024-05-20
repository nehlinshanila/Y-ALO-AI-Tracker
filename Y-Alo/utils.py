import datetime

# Validate date function
def validate_date(date_text: str) -> bool:
    try:
        datetime.datetime.strptime(date_text, '%Y-%m-%d')
        return True
    except ValueError:
        return False
