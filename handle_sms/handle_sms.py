import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail, Content

sendgrid_api = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))


def phone_to_email(potential_number):

    # Converts a phone number like +14155551212
    # into an email address like 14155551212@sms.example.com

    phone_number = potential_number.replace('+', '')
    return"{}@{}".format(phone_number, os.environ.get('EMAIL_DOMAIN'))


def lambda_handler(event, context):

    payload = event.get("data", {})

    message = Mail(
        from_email=phone_to_email(payload.get('From')),
        to_emails='rohail_najam@hotmail.com',
        subject='Text message',
        plain_text_content= Content("text/plain", payload.get('Body'))
    )
    response = sendgrid_api.send(message)

    return '<Response> {} </Response>'.format(response.body)

