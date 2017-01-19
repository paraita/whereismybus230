#!/usr/bin/env python
# -*- coding: utf-8 -*-
import datetime

from dateutil.tz import tzfile
from flask import json
from .main import app
import unittest
from unittest.mock import patch


class MainApiTests(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    @patch('sophiabus230.get_next_buses')
    def test_get_no_buses(self, mock_bus):
        mock_bus.return_value = []
        result = self.app.get('/bus230')
        json_data = json.loads(result.data)
        self.assertEqual(json_data, [])
        self.assertEqual(result.status_code, 200)

    @patch('sophiabus230.get_next_buses')
    def test_get(self, mock_bus):

        expected_tt = [
            {'dest': 'Cathédrale-Vieille Ville',
             'is_real_time': True,
             'bus_time': '2017-01-19T17:23:06.302989+01:00'
             },
            {'dest': 'Cathédrale-Vieille Ville',
             'is_real_time': False,
             'bus_time': '2017-01-19T17:32:00'
             }
            ]
        mock_bus.return_value = [
            {'dest': b'Cath\xc3\xa9drale-Vieille Ville',
             'is_real_time': True,
             'bus_time': datetime.datetime(2017, 1, 19, 17, 23, 6, 302989,
                                           tzinfo=tzfile('/usr/share/zoneinfo/Europe/Paris'))
             },
            {'dest': b'Cath\xc3\xa9drale-Vieille Ville',
             'is_real_time': False,
             'bus_time': datetime.datetime(2017, 1, 19, 17, 32)
             }
            ]
        result = self.app.get('/bus230')
        json_data = json.loads(result.data)
        self.assertEqual(json_data, expected_tt)
        self.assertEqual(result.status_code, 200)
