import csv
import os
from base64 import b64encode
from datetime import datetime
from logging import getLogger

from constance import config
from django.conf import settings
from django.core.files import File
from requests import request, get

from utils.utils import get_current_site_no_request

logger = getLogger(__name__)


class SendInBlueService:

    @classmethod
    def send_email(cls, data, template_id):
        url = f'https://api.sendinblue.com/v3/smtp/email'

        payload = {
            'to': data.get('to'),
            'templateId': template_id,
        }

        bcc = data.get('bcc', None)
        if bcc:
            payload.update({'bcc': bcc})

        attachment = data.get('attachment', None)
        if attachment:
            if attachment.get('url') == 'in_memory':
                if "content_bytes" in attachment:
                    attachment_b64 = b64encode(attachment.get('content_bytes'))
                else:
                    attachment_b64 = b64encode(attachment.get('content').getvalue().encode())
            else:
                attachment_b64 = b64encode(get(attachment.get('url')).content)

            payload.update({
                'attachment': [
                    {
                        'content': attachment_b64.decode(),
                        'name': attachment.get('name')
                    }
                ]
            })
        
        params = data.get('params', None)
        if params:
            payload.update({'params': params})

        headers = {
            'Accept': "application/json",
            'Origin': get_current_site_no_request().domain,
            'api-key': config.SENDINGBLUE_API_KEY,
            'Content-Type': "application/json",
            'cache-control': "no-cache",
        }        

        if not config.SEND_EMAILS:
            logger.debug('sendinblue append csv')
            SendInBlueService.create_csv_mailing(url, payload, headers)
        else:
            logger.info(f'sendinblue url: {url}')
            logger.info(f'sendinblue payload: {str(payload)}')
            logger.info(f'sendinblue headers: {str(headers)}')
            req = request("POST", url, json=payload, headers=headers)
            logger.info(f'sendinblue status_code: {req.status_code}')
            logger.info(f'sendinblue body: {req.text}')
            return req

    @classmethod
    def create_csv_mailing(cls, url, payload, headers):
        local_path = 'tmp/emails/'
        filename = 'emails.csv'
        if not os.path.exists(local_path):
            os.makedirs(local_path)

        with open(local_path + filename, 'a+') as f:
            file = File(f)
            writer = csv.writer(file)

            date_now = datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
            writer.writerow(['Date: ' + date_now])
            writer.writerow(['Url: ' + url])
            writer.writerow(['Payload: ' + str(payload)])
            writer.writerow(['Headers: ' + str(headers)])
            writer.writerow([])
            writer.writerow([])
