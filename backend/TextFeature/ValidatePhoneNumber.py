import re

def contains_phone_number(phone_number):
    # Define a regular expression pattern for a U.S. phone number
    pattern = r"^(?:\+1\s?)?\d{3}[-.\s]?\d{3}[-.\s]?\d{4}$"

    # Use the re.match() function to check if the input matches the pattern
    if re.match(pattern, phone_number):
        return True
    else:
        return False