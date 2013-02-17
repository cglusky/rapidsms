import copy
import requests
import logging

from django.utils import simplejson as json

from rapidsms.backends.base import BackendBase


logger = logging.getLogger(__name__)


class VumiBackend(BackendBase):
    """Outgoing SMS backend for Vumi."""

    def configure(self, sendsms_url, sendsms_params=None, **kwargs):
        self.sendsms_url = sendsms_url
        self.sendsms_params = sendsms_params or {}

    def prepare_request(self, id_, text, identities, context):
        """Construct outbound data for requests.post."""
        kwargs = {'url': self.sendsms_url,
                  'headers': {'content-type': 'application/json'}}
        payload = copy.copy(self.sendsms_params)
        payload.update({'content': text, 'to_addr': identities,
                        'session_event': None})
        if 'external_id' in context:
            payload['in_reply_to'] = context['external_id']
        kwargs['data'] = json.dumps(payload)
        return kwargs

    def send(self, id_, text, identities, context={}):
        logger.info('Sending message: %s' % text)
        kwargs = self.prepare_request(id_, text, identities, context)
        r = requests.post(**kwargs)
        logger.debug(r)
