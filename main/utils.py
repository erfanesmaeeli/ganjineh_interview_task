
from django.core.mail import EmailMessage
from django.template.loader import get_template
from datetime import datetime


def send_email(data, to_user, subject, email_template):
    email_message = get_template(email_template).render(data)
    msg = EmailMessage(
        subject,
        email_message,
        'Erfan Test <info@erffan.com>',
        [to_user]
    )
    msg.content_subtype = "html"
    msg.send()



def custom_date_parser(date_str):
    date_formats = [
        "%d-%m-%y", "%d/%m/%y", "%d.%m.%y",
        "%Y-%m-%d", "%Y/%m/%d", "%Y.%m.%d",
        "%m-%d-%y", "%m/%d/%y", "%m.%d.%y",
        "%y-%m-%d", "%y/%m/%d", "%y.%m.%d",
        "%m-%d-%Y", "%m/%d/%Y", "%m.%d.%Y",
    ]

    normalized_date_str = date_str.replace("/", "-").replace(".", "-")
    
    for fmt in date_formats:
        try:
            return datetime.strptime(normalized_date_str, fmt)
        except ValueError:
            continue