
from FARMWARE import FARMWARE
from CeleryPy import log


FARMWARE_NAME = "Test-Farmware"


if __name__ == "__main__":

    log('Start script.py...', message_type='info', title=FARMWARE_NAME)
	
    try:
        farmware = FARMWARE(FARMWARE_NAME)
    except Exception as e:
        #log(type(e).__str__ + ' ' + e.args + ' ' + e ,message_type='error', title=FARMWARE_NAME + " : init" )
        log(e ,message_type='error', title=FARMWARE_NAME + " : init" )
    else:
        try:
            #farmware.run()
            pass
        except Exception as e:
            log(e ,message_type='error', title=FARMWARE_NAME + " : run" )    
    
    log('End script.py...', message_type='info', title=FARMWARE_NAME)
