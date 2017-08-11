from django.conf import settings
from django.template.loader import get_template
from django.core.mail import EmailMultiAlternatives


def send_unique_email(subject, message, recipient, template_for_html_message='mail_notifications/default.html'):
    context = {
        'message': message
    }

    subject = subject
    message = message
    from_email = settings.DEFAULT_FROM_EMAIL
    to = recipient
    html_content = get_template(template_for_html_message).render(context)
    msg = EmailMultiAlternatives(subject, message, from_email, [to])
    msg.attach_alternative(html_content, "text/html")
    msg.send()