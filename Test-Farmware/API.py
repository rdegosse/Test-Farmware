import os
import sys
import json
import base64
import requests
import CeleryPy
import re

from CeleryPy import log

class API():     

    def api_setup(self):
         # API requests setup
        try:
            api_token = os.environ['API_TOKEN']
        except KeyError:
            api_token = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJhdWQiOiJib3QiLCJzdWIiOjE0NiwiaWF0IjoxNTE3NTY4NjI5LCJqdGkiOiI4MTRjODkzZi1lMGQzLTRhMGMtOGZkNi03ODc0ZWE4NmE1YjkiLCJpc3MiOiIvLzEwLjEuMS45MDozMDAwIiwiZXhwIjoxNTIxMDI0NjI5LCJtcXR0IjoiMTAuMS4xLjkwIiwiYm90IjoiZGV2aWNlXzIxMSIsInZob3N0IjoiLyIsIm1xdHRfd3MiOiJ3czovLzEwLjEuMS45MDozMDAyL3dzIiwib3NfdXBkYXRlX3NlcnZlciI6Imh0dHBzOi8vYXBpLmdpdGh1Yi5jb20vcmVwb3MvRmFybUJvdC9mYXJtYm90X29zL3JlbGVhc2VzLzkyMDA5NDMiLCJpbnRlcmltX2VtYWlsIjoicmRlZ29zc2VAaW5pdGhpbmsuZnIiLCJmd191cGRhdGVfc2VydmVyIjoiREVQUkVDQVRFRCIsImJldGFfb3NfdXBkYXRlX3NlcnZlciI6Ik5PVF9TRVQifQ.K8Fv-Y2XuOEa_1ZoiwO3MZYk5X4FT8tvG6UKj2GTzwq2KpGU28DySaUa7z2AnfxI_L50Yuc2GviHVKkrhFAzum4mRKXpzIBkpHnLUSc_VvPdsYIXrU_cDn5nTDrZoO_okje0hepp6SBPtCyuimf6iijpergVCNUj8w-SNuft62ZnE_0f1JI8glTjCOSuPIVAoZmlYb2sd8_m9OSivqHbagunql2uAsgfY5-88Xsh7cn5fy04S_f04-AEi3iyEqchGjlfxWu7rPuPg7jSGbv0hYzBR36H2C2YOfbPrRQlleD5kom7JXYDlrdJPV3d48NlB3SJQGxtYYM9XmafAtf2YQ'

        try:
            encoded_payload = api_token.split('.')[1]
            encoded_payload += '=' * (4 - len(encoded_payload) % 4)
            json_payload = base64.b64decode(encoded_payload).decode('utf-8')
            server = json.loads(json_payload)['iss']
        except:  
            server = '//my.farmbot.io'

        self.api_url = 'http{}:{}/api/'.format(
            's' if 'localhost' not in server and not re.compile('^//((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\\.){3}(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)').match(server) else '', server)
        self.headers = {'Authorization': 'Bearer {}'.format(api_token),
                        'content-type': "application/json"}
        
        log(self.api_url, message_type='debug', title='Class API:api_setup')
        log(self.headers, message_type='debug', title='Class API:api_setup')
        log(json_payload, message_type='debug', title='Class API:api_setup')

    def __init__(self,farmware):
        self.farmwarename = farmware.farmwarename
        self.api_setup()

    def api_get(self, endpoint):
        """GET from an API endpoint."""
        response = requests.get(self.api_url + endpoint, headers=self.headers)
        self.api_response_error_collector(response)
        self.api_response_error_printer()
        return response.json()

    def api_response_error_collector(self, response):
        """Catch and log errors from API requests."""
        self.errors = {}  # reset
        if response.status_code != 200:
            try:
                self.errors[str(response.status_code)] += 1
            except KeyError:
                self.errors[str(response.status_code)] = 1

    def api_response_error_printer(self):
        """Print API response error output."""
        error_string = ''
        for key, value in self.errors.items():
            error_string += '{} {} errors '.format(value, key)
        if error_string != '':
            log(error_string, message_type='error', title='Class API:api_response_error_printer')