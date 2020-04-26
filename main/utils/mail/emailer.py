import logging
import time
import sendgrid
from sendgrid.helpers.mail import (
    Mail, Content, To, Subject, Substitution,
    MimeType, TemplateId, From, DynamicTemplateData
)
from python_http_client import exceptions

from django.conf import settings

logger = logging.getLogger(__name__)

sg = sendgrid.SendGridAPIClient(getattr(settings, 'SENDGRID_API_KEY'))

class Emailer(object):
    def __init__(self):
        super().__init__()

    def _compose(self, template_id):
        self.message.content = Content(MimeType.html, '<strong>Maquis Bernadette</strong>')
        self.message.template_id = TemplateId(template_id)
        self.message.from_email = From(getattr(settings, 'FROM_EMAIL'), 'Maquis Bernadette')

    def add_personalization(self, tos, subject, template_data, index):
        self.message.to = [To(to, '', p=index) for to in tos]
        self.message.subject = Subject(subject, p=index)
        self.message.dynamic_template_data = DynamicTemplateData(template_data, p=index)

    def send(self):
        try:
            response = sg.send(message=self.message.get())
            return response.status_code
        except (exceptions.InternalServerError, exceptions.ServiceUnavailableError,
                exceptions.TooManyRequestsError) as e:
            time.sleep(60)
            self.send()
        except exceptions.BadRequestsError as e:
            logger.exception('[EXCEPTION] Bad request')
            raise(Exception(e.reason))
        except Exception as e:
            raise(e)

class ClientEmailer( Emailer ):
    def __init__(self):
        super().__init__()

    def send_order(self, order):
        template_id = getattr(settings, 'TEMPLATE_ORDER_ID')
        self.message = Mail()
        self._compose(template_id)
        self.add_personalization(
            [getattr(settings, 'TO_EMAIL')],
            'Maquis Bernadette - Order',
            {
                'subject': 'Maquis Bernadette - Order',
                'nom': order['nom'],
                'address': order['address'],
                'tel': order['tel'],
                'num_poulet_braise': order['num_poulet_braise'],
                'num_kedjenou_poulet': order['num_kedjenou_poulet'],
                'num_poisson_braise': order['num_poisson_braise'],
                'num_kedjenou_poisson': order['num_kedjenou_poisson']
            },
            0
        )
        self.send()