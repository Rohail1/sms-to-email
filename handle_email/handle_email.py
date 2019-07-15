import os
import json
import base64
from requests_toolbelt.multipart import decoder
from twilio.rest import Client

client = Client(os.environ.get('TWILIO_ACCOUNT_SID'), os.environ.get('TWILIO_AUTH_TOKEN'))


def lambda_handler(event, context):
    print(event)
    body = event.get('body')
    bytes_body = base64.b64decode(body)
    print('bytes_body :: ', bytes_body)
    content_type = event['headers'].get('Content-Type')
    print('content :: ',  content_type)
    multipart_data = decoder.MultipartDecoder(bytes_body, content_type)
    number = 0
    text_message = ''
    for part in multipart_data.parts:

        if b'envelop' in part.headers[b'Content-Disposition']:
            number_array = json.loads(part.content.decode('utf-8'))['to'][0].split("@")
            number = '+{}'.format(number_array[0])

        if b'text' in part.headers[b'Content-Disposition']:
            text_message = part.text.lstrip().rstrip()

    sms = {
        'to': number,
        'from_': os.environ.get('TWILIO_NUMBER'),
        'body': text_message
    }

    try:
        message = client.messages.create(**sms)

        payload = {
            "status": True,
            "message_id": message.sid
        }
        print(payload)
        return payload
    except Exception as e:
        payload ={
            "status": False,
            "error": str(e)
        }

        print(payload)
        return payload
