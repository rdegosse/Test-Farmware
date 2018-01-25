import os
import sys


from CeleryPy import log
# from DB import DB




if __name__ == "__main__":

    log('Start script.py...', message_type='info', title='Test-Farmware')
	
    try:
        api_token = os.environ['API_TOKEN']
    except KeyError:
        api_token = 'no token'
			
    log(api_token, message_type='info', title='Test-Farmware')
	
    try:
        api_host = os.environ['API_HOST']
    except KeyError:
        api_host = 'no api host'
	
    log(api_host, message_type='info', title='Test-Farmware')

#    plantdb= DB()

 #   plantdb.load_plants_from_web_app()   #Get plant points from Webapp
 #   plantdb.count_downloaded_plants()    #Print Plantcount in log
 #   plantdb.load_sequences_from_app()    #Get sequences and determine the sequence id
 #   plantdb.loop_plant_points()          #Move to plant points and water them with the Water on/off sequence

 
    log('End script.py...', message_type='info', title='Test-Farmware')