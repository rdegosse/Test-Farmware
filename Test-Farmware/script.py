import os
import sys
import json
import base64
import requests

from CeleryPy import log
from Util import *

# from DB import DB


if __name__ == "__main__":

    log('Start script.py...', message_type='info', title='Test-Farmware')
	
    try:
        api_token = os.environ['API_TOKEN']
    except KeyError:
        api_token = 'no token'
        api_token = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJhdWQiOiJib3QiLCJzdWIiOjE0NiwiaWF0IjoxNTE3NTY4NjI5LCJqdGkiOiI4MTRjODkzZi1lMGQzLTRhMGMtOGZkNi03ODc0ZWE4NmE1YjkiLCJpc3MiOiIvLzEwLjEuMS45MDozMDAwIiwiZXhwIjoxNTIxMDI0NjI5LCJtcXR0IjoiMTAuMS4xLjkwIiwiYm90IjoiZGV2aWNlXzIxMSIsInZob3N0IjoiLyIsIm1xdHRfd3MiOiJ3czovLzEwLjEuMS45MDozMDAyL3dzIiwib3NfdXBkYXRlX3NlcnZlciI6Imh0dHBzOi8vYXBpLmdpdGh1Yi5jb20vcmVwb3MvRmFybUJvdC9mYXJtYm90X29zL3JlbGVhc2VzLzkyMDA5NDMiLCJpbnRlcmltX2VtYWlsIjoicmRlZ29zc2VAaW5pdGhpbmsuZnIiLCJmd191cGRhdGVfc2VydmVyIjoiREVQUkVDQVRFRCIsImJldGFfb3NfdXBkYXRlX3NlcnZlciI6Ik5PVF9TRVQifQ.K8Fv-Y2XuOEa_1ZoiwO3MZYk5X4FT8tvG6UKj2GTzwq2KpGU28DySaUa7z2AnfxI_L50Yuc2GviHVKkrhFAzum4mRKXpzIBkpHnLUSc_VvPdsYIXrU_cDn5nTDrZoO_okje0hepp6SBPtCyuimf6iijpergVCNUj8w-SNuft62ZnE_0f1JI8glTjCOSuPIVAoZmlYb2sd8_m9OSivqHbagunql2uAsgfY5-88Xsh7cn5fy04S_f04-AEi3iyEqchGjlfxWu7rPuPg7jSGbv0hYzBR36H2C2YOfbPrRQlleD5kom7JXYDlrdJPV3d48NlB3SJQGxtYYM9XmafAtf2YQ'
			
    log(api_token, message_type='info', title='Test-Farmware')
	
    try:
        encoded_payload = api_token.split('.')[1]
        encoded_payload += '=' * (4 - len(encoded_payload) % 4)
        log("encoded_payload:" + encoded_payload, message_type='info', title='Test-Farmware')
        
        
        json_payload = base64.b64decode(encoded_payload).decode('utf-8')
        server = json.loads(json_payload)['iss']
        log("json_payload:" + json_payload, message_type='info', title='Test-Farmware')
        
    except:  
        server = '//my.farmbot.io'
    
    api_url = 'http{}:{}/api/'.format('', server)
    log(api_url, message_type='info', title='Test-Farmware')
    
    headers = {'Authorization': 'Bearer {}'.format(api_token),'content-type': "application/json"}        
    log(headers, message_type='info', title='Test-Farmware')
    
    
    response = requests.get(api_url + 'points', headers=headers)
    app_points = response.json()
    if response.status_code == 200:
        #app_points = Filter_Points(app_points,openfarm_slug='carrot')
        app_points = Filter_Points(app_points)
        log(len(app_points), message_type='debug', title='Test-Farmware')

        opt_points,tab_id = Get_Optimal_Way(app_points)
        log(len(opt_points), message_type='debug', title='Test-Farmware')
        log(len(tab_id), message_type='debug', title='Test-Farmware')
        log(tab_id, message_type='debug', title='Test-Farmware')
        #log(opt_points, message_type='info', title='Test-Farmware')

        for p in opt_points:
            log(p, message_type='debug', title='Test-Farmware')    

        #log('', message_type='info', title='Test-Farmware')
        #log(len(app_points), message_type='info', title='Test-Farmware')
        #log(app_points, message_type='info', title='Test-Farmware')
        #log('', message_type='info', title='Test-Farmware')
        #log(len(tab_id), message_type='info', title='Test-Farmware')
        #log(tab_id, message_type='info', title='Test-Farmware')
        #log('', message_type='info', title='Test-Farmware')
        #log(len(opt_points), message_type='info', title='Test-Farmware')
        #log(opt_points, message_type='info', title='Test-Farmware')
    
    
    log('End script.py...', message_type='info', title='Test-Farmware')
