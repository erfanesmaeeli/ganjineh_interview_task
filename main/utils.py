
from django.core.mail import EmailMessage
from django.template.loader import get_template


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