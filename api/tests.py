import json
import datetime

from django.test import TestCase
from django.contrib.auth import get_user_model
from django.conf import settings
from django.urls import reverse, resolve

from rest_framework import status
from rest_framework.test import APIClient

class MBTests( TestCase ):
    def setUp(self):
        self.client = APIClient()

    def test_sending_orders(self):
        payload = {
            'nom': 'Stephane',
            'address': 'Begneri carrefour des trucs',
            'tel': '+233209456202',
            'num_poulet_braise': 2,
            'num_kedjenou_poulet': 1,
            'num_poisson_braise': 0,
            'num_kedjenou_poisson': 0
        }

        response = self.client.post(
            reverse('orders_send'),
            data=json.dumps(payload),
            content_type='application/json'
        )
        results = json.loads(response.content.decode('utf-8'))
        print( 'result--->>', results )
        self.assertEqual(response.status_code, status.HTTP_200_OK)