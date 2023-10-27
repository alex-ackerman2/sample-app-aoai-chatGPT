import re
def contains_phone_number(input_string):
    # Regular expression pattern to match common phone number formats
    phone_number_pattern = r'\d{9}'
    
    # Search for the phone number pattern in the input string
    match = re.search(phone_number_pattern, input_string)
    
    # Check if the pattern is found
    if match:
        return True
    else:
        return False