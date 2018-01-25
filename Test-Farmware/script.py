import os
import sys


from CeleryPy import log
# from DB import DB




if __name__ == "__main__":

    log('Start script.py...', message_type='info', title='Test-Farmware')

 #   log(os.environ['API_TOKEN'], message_type='info', title='Test-Farmware')
	
#	log(os.environ['API_HOST'], message_type='info', title='Test-Farmware')

#    plantdb= DB()

 #   plantdb.load_plants_from_web_app()   #Get plant points from Webapp
 #   plantdb.count_downloaded_plants()    #Print Plantcount in log
 #   plantdb.load_sequences_from_app()    #Get sequences and determine the sequence id
 #   plantdb.loop_plant_points()          #Move to plant points and water them with the Water on/off sequence

 
    log('End script.py...', message_type='info', title='Test-Farmware')