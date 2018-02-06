
from FARMWARE import MyFarmware
from CeleryPy import log



if __name__ == "__main__":

    FARMWARE_NAME = "Test-Farmware"

    log('Start script.py...', message_type='debug', title=FARMWARE_NAME)
    
    
    try:
        farmware = MyFarmware(FARMWARE_NAME)
        #pass
    except Exception as e:
        log(e ,message_type='error', title=FARMWARE_NAME + " : init" )
        raise Exception(e)
    else:
        try:
            farmware.run()
            #pass
        except Exception as e:
            log(e ,message_type='error', title=FARMWARE_NAME + " : run" )
            #raise Exception(e)
    

    log('End script.py...', message_type='debug', title=FARMWARE_NAME)

