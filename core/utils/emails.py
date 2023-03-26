import csv
import os

from celery import shared_task
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.utils import translation
from django.conf import settings


@shared_task
def email_account_info(
        mail_subject,
        email_template,
        username,
        tenant_domain,
        to_email,
        instance,
        language=None
):
    prev_language = translation.get_language()
    try:
        language and translation.activate(language)
        message = render_to_string(email_template, {
            'instance': instance,
            'user': username,
            'domain': tenant_domain,
            'email': to_email,
        })
        to_email = to_email
        email = EmailMessage(mail_subject, message, to=[to_email])
        email.send()
    except Exception as e:
        print(e)
    finally:
        translation.activate(prev_language)


@shared_task
def email_new_account_info(mail_subject,
                           email_template,
                           username,
                           domain,
                           to_email,
                           language=None):
    prev_language = translation.get_language()
    try:
        language and translation.activate(language)
        message = render_to_string(email_template, {
            'user': username,
            'domain': domain,
            'email': to_email,
        })
        to_email = to_email
        email = EmailMessage(mail_subject, message, to=[to_email])
        email.send()
    except Exception as e:
        print(e)
    finally:
        translation.activate(prev_language)


@shared_task
def prospect_confirm_email_info(
        mail_subject,
        email_template,
        username,
        front_domain,
        to_email,
        token,
        prospect_uuid,
        language=None):

    prev_language = translation.get_language()
    try:
        language and translation.activate(language)
        message = render_to_string(email_template, {
            'prospect_uuid': prospect_uuid,
            'user': username,
            'domain': front_domain,
            'token': token,
            'email': to_email,
        })
        to_email = to_email
        email = EmailMessage(mail_subject, message, to=[to_email])
        email.send()
    except Exception as e:
        print(e)
    finally:
        translation.activate(prev_language)


@shared_task
def email_contact_message(name, phone, email, country, mail_subject, content, to_email, email_template, language=None):
    prev_language = translation.get_language()
    try:
        language and translation.activate(language)
        message = render_to_string(email_template,
                                   {'name': name, 'phone': phone, 'message': content,
                                    'country': country, 'email': email})
        to_email = to_email
        email = EmailMessage(mail_subject, message,  to=[to_email])
        email.send()
    except Exception as e:
        print(e)
    finally:
        translation.activate(prev_language)


@shared_task
def email_bug_message(full_name, bug_type, mail_subject, message, to_email, email_template, language=None):
    prev_language = translation.get_language()
    try:
        language and translation.activate(language)
        message = render_to_string(email_template,
                                   {'full_name': full_name, 'bug_type': bug_type, 'message': message})
        to_email = to_email
        email = EmailMessage(mail_subject, message, to=[to_email])
        email.send()
    except Exception as e:
        print(e)
    finally:
        translation.activate(prev_language)


@shared_task
def send_password_reset_link(email_template, mail_subject, to_email, context, language=None):
    prev_language = translation.get_language()
    try:
        language and translation.activate(language)
        message = render_to_string(email_template, context)
        to_email = to_email
        email = EmailMessage(mail_subject, message, to=[to_email])
        email.send()
    except Exception as e:
        print(e)
    finally:
        translation.activate(prev_language)


@shared_task
def send_password_reset_link(email_template, mail_subject, to_email, context, language=None):
    prev_language = translation.get_language()
    try:
        language and translation.activate(language)
        message = render_to_string(email_template, context)
        to_email = to_email
        email = EmailMessage(mail_subject, message, to=[to_email])
        email.send()
    except Exception as e:
        print(e)
    finally:
        translation.activate(prev_language)


@shared_task
def send_alert_email(email_template, mail_subject, to_email, context, language=None):
    prev_language = translation.get_language()
    try:
        language and translation.activate(language)
        message = render_to_string(email_template, context)
        to_email = to_email
        email = EmailMessage(mail_subject, message, to=[to_email])
        email.send()
    except Exception as e:
        print(e)
    finally:
        translation.activate(prev_language)


@shared_task
def email_new_prospect(email_template, mail_subject, to_email, context, language=None):
    prev_language = translation.get_language()
    try:
        language and translation.activate(language)
        message = render_to_string(email_template, context)
        to_email = to_email
        email = EmailMessage(mail_subject, message, to=[to_email])
        email.send()
    except Exception as e:
        print(e)
    finally:
        translation.activate(prev_language)


@shared_task
def email_new_approval_request(email_template, 
                                mail_subject, 
                                to_email, 
                                context, 
                                language=None):
    prev_language = translation.get_language()
    try:
        language and translation.activate(language)
        message = render_to_string(email_template, context)
        to_email = to_email
        email = EmailMessage(mail_subject, message, to=[to_email])
        email.send()
    except Exception as e:
        print(e)
    finally:
        translation.activate(prev_language)

def email_csv(f, mail_subject, message, to_email):
    mail = EmailMessage(mail_subject, message, to=[to_email])
    with open(f.name, "r") as fr:
        # CustomEmailMessage(email_subject, email_body, email_from, to=email_to, bcc=[])
        mail.attach(os.path.basename(f.name), fr.read(), "application/octet-stream")
        # mail.set_content(os.path.basename(fr.read())
    mail.send()


@shared_task
def write_and_email_csv_errors(data, file_path, context, mode="w+"):
    mail_subject = context.get("mail_subject")
    message = context.get("message")
    to_email = context.get("to_email")
    mail = EmailMessage(mail_subject, message, to=[to_email])
    with open(file_path, mode, newline="") as f:
        file_writer = csv.writer(f, delimiter=",", lineterminator="\n")
        file_header = data[0].keys()
        file_writer.writerow(list(file_header))
        for row in data:
            file_writer.writerow([val for val in row.values()])
        f.close()
    with open(file_path, "rb") as fr:
        mail.attach(file_path, fr.read(), 'text/csv')
        fr.close()
    mail.send()


def send_email(instance, user, language=None):
    email_template = 'tasks/task_assigned_email_alert.html'
    mail_subject = 'Task alert: ' + instance.subject
    domain = os.environ.get("FRONT_URL", settings.FRONT_URL)
    task_id = instance.id
    task_uuid = instance._id
    message = instance.detail

    context = {}
    to_email = user.email
    context['username'] = user.name
    context['task_id'] = task_id
    context['task_uuid'] = task_uuid
    context['domain'] = domain
    context['message'] = message
    send_alert_email.delay(email_template, mail_subject, to_email, context, language=language)
    instance.users_notified.add(user)


@shared_task
def email_booking_receipt(mail_subject, to_email, email_template, context, language=None):
    prev_language = translation.get_language()
    try:
        language and translation.activate(language)
        message = render_to_string(email_template,
                                   context)
        to_email = to_email
        email = EmailMessage(mail_subject, message, to=[to_email])
        email.send()
    except Exception as e:
        print(e)
    finally:
        translation.activate(prev_language)