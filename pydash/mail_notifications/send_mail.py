from django.conf import settings
from django.template.loader import get_template
from django.core.mail import EmailMultiAlternatives, get_connection


def send_unique_email(subject, message, recipient, template_for_html_message='mail_notifications/default.html', solved=False):
    if solved:
        context = {
            'message': message,
            'solved': True
        }
    else:
        context = {
            'message': message,
        }


    subject = subject
    message = message
    from_email = settings.DEFAULT_FROM_EMAIL
    to = recipient
    html_content = get_template(template_for_html_message).render(context)
    msg = EmailMultiAlternatives(subject, message, from_email, [to])
    msg.attach_alternative(html_content, "text/html")
    msg.send()


def send_mass_email(messages_tuple_list,template_for_html_message='mail_notifications/default.html', solved=False):
    messages_list = []

    for i in messages_tuple_list:
        message = i[1]

        if solved:
            context = {
                'message': message,
                'solved': True
            }
        else:
            context = {
                'message': message,
            }

        subject = i[0]

        from_email = settings.DEFAULT_FROM_EMAIL
        to = i[2]
        html_content = get_template(template_for_html_message).render(context)
        msg = EmailMultiAlternatives(subject, message, from_email, [to])
        msg.attach_alternative(html_content, "text/html")
        messages_list.append((msg))

    connection = get_connection()
    connection.open()

    for m in messages_list:
        m.send()

    connection.close()


