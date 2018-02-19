import os

from FARMWARE import MyFarmware
from CeleryPy import log
from CeleryPy import read_status

from ENV import redis_load
from ENV import load


if __name__ == "__main__":

    FARMWARE_NAME = "Test-Farmware"

    log('Start...', message_type='info', title=FARMWARE_NAME)

    #log(read_status(), message_type='info', title=FARMWARE_NAME)

    #log(os.environ.get('FARMWARE_URL','not set'), message_type='info', title=FARMWARE_NAME)
    
    log(redis_load(key='location.position',name='x'), message_type='info', title=FARMWARE_NAME)
    log(load(name='location'), message_type='info', title=FARMWARE_NAME)

    """
    try:
        farmware = MyFarmware(FARMWARE_NAME)
    except Exception as e:
        log(e ,message_type='error', title=FARMWARE_NAME + " : init" )
        raise Exception(e)
    else:
        try:
            farmware.run()
        except Exception as e:
            log(e ,message_type='error', title=FARMWARE_NAME + " : run" )
            raise Exception(e)
    
    """
    log('End...', message_type='info', title=FARMWARE_NAME)

