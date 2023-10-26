import email, smtplib, ssl

def validate_number(number: str):
    num = ""
    valid = False

    for character in number:
        if character.isdigit():
            num += character

    # a phone number will have a valid length of 10 digits as all of the phone
    # domains are US phone domains with area codes

    if len(num) == 10:
        valid = True

    if not valid:
        raise NumberNotValidException(number)

    return num


def format_provider_email_address(number: str, provider: str, mms=False):
    provider_info = PROVIDERS.get(provider)

    if provider_info == None:
        raise ProviderNotFoundException(provider)

    domain = provider_info.get("sms")

    if mms:
        mms_support = provider_info.get("mms_support")
        mms_domain = provider_info.get("mms")

        if not mms_support:
            raise NoMMSSupportException(provider)

        # use mms domain if provider has one
        if mms_domain:
            domain = mms_domain

    return f"{number}@{domain}"


def send_sms_via_email(
    number: str,
    message: str,
    provider: str,
    sender_credentials: tuple = ("electrodes.test@gmail.com", "uyzr pldp mfhp akzw"),
    subject: str = "Sent Through Text via Email",
    smtp_server: str = "smtp.gmail.com",
    smtp_port: int = 465,
):
    number = validate_number(number)
    sender_email, email_password = sender_credentials
    receiver_email = format_provider_email_address(number, provider)

    email_message = f"To:{receiver_email}\r\n\r\n{message}"

    with smtplib.SMTP_SSL(
        smtp_server, smtp_port, context=ssl.create_default_context()
    ) as email:
        email.login(sender_email, email_password)
        email.sendmail(sender_email, receiver_email, email_message)


class ProviderNotFoundException(Exception):
    def __init__(self, provider: str):
        self.provider = provider

    def __str__(self):
        return (
            f"{self.provider} not found. The valid provider options are\n"
            f"{', '.join(PROVIDERS.keys())}"
        )


class NoMMSSupportException(Exception):
    def __init__(self, provider: str):
        self.provider = provider

    def __str__(self):
        return f"{self.provider} does not support mms"


class NumberNotValidException(Exception):
    def __init__(self, number: str):
        self.number = number

    def __str__(self):
        return (
            f"{self.number} not valid. "
            "It must be a valid US phone number 10 digits in length."
        )     

PROVIDERS = {
    "AT&T": {"sms": "txt.att.net", "mms": "mms.att.net", "mms_support": True},
    "Boost Mobile": {
        "sms": "sms.myboostmobile.com",
        "mms": "myboostmobile.com",
        "mms_support": True,
    },
    "C-Spire": {"sms": "cspire1.com", "mms_support": False},
    "Cricket Wireless": {
        "sms": "sms.cricketwireless.net ",
        "mms": "mms.cricketwireless.net",
        "mms_support": True,
    },
    "Consumer Cellular": {"sms": "mailmymobile.net", "mms_support": False},
    "Google Project Fi": {"sms": "msg.fi.google.com", "mms_support": True},
    "Metro PCS": {"sms": "mymetropcs.com", "mms_support": True},
    "Mint Mobile": {"sms": "mailmymobile.net", "mms_support": False},
    "Page Plus": {
        "sms": "vtext.com",
        "mms": "mypixmessages.com",
        "mms_support": True,
    },
    "Republic Wireless": {
        "sms": "text.republicwireless.com",
        "mms_support": False,
    },
    "Sprint": {
        "sms": "messaging.sprintpcs.com",
        "mms": "pm.sprint.com",
        "mms_support": True,
    },
    "Straight Talk": {
        "sms": "vtext.com",
        "mms": "mypixmessages.com",
        "mms_support": True,
    },
    "T-Mobile": {"sms": "tmomail.net", "mms_support": True},
    "Ting": {"sms": "message.ting.com", "mms_support": False},
    "Tracfone": {"sms": "", "mms": "mmst5.tracfone.com", "mms_support": True},
    "U.S. Cellular": {
        "sms": "email.uscc.net",
        "mms": "mms.uscc.net",
        "mms_support": True,
    },
    "Verizon": {"sms": "vtext.com", "mms": "vzwpix.com", "mms_support": True},
    "Virgin Mobile": {
        "sms": "vmobl.com",
        "mms": "vmpix.com",
        "mms_support": True,
    },
    "Xfinity Mobile": {
        "sms": "vtext.com",
        "mms": "mypixmessages.com",
        "mms_support": True,
    },
} 
