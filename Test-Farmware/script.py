import os
import sys
import json
import base64
import requests

from CeleryPy import log
from Util import get_optimal_way

# from DB import DB


if __name__ == "__main__":

    log('Start script.py...', message_type='info', title='Test-Farmware')
	
    try:
        api_token = os.environ['API_TOKEN']
    except KeyError:
        api_token = 'no token'
			
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
            opt_points, tab_id = get_optimal_way(app_points)
    
    log(tab_id, message_type='info', title='Test-Farmware')
    
    
    
#    plantdb= DB()

 #   plantdb.load_plants_from_web_app()   #Get plant points from Webapp
 #   plantdb.count_downloaded_plants()    #Print Plantcount in log
 #   plantdb.load_sequences_from_app()    #Get sequences and determine the sequence id
 #   plantdb.loop_plant_points()          #Move to plant points and water them with the Water on/off sequence

 
    log('End script.py...', message_type='info', title='Test-Farmware')
