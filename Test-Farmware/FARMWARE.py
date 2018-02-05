import os

from API import API
from UTIL import *
from CeleryPy import log

class FARMWARE():

    def get_input_env(self):
        prefix = self.farmwarename.lower().replace('-','_')
        
        self.input_pointname = os.environ.get(prefix+"_pointname", "")
        self.input_openfarm_slug = os.environ.get(prefix+"_openfarm_slug", "")
        self.input_age_min_day = os.environ.get(prefix+"__age_min_day", 0)
        self.input_age_max_day = os.environ.get(prefix+"__age_max_day", 365)
        self.input_filter_meta_key = os.environ.get(prefix+"_filter_meta_key", "")
        self.input_filter_meta_value = os.environ.get(prefix+"_filter_meta_value", "")
        self.input_sequence_init = os.environ.get(prefix+"_sequence_init", "Not Set")
        self.input_sequence_beforemove  = os.environ.get(prefix+"_sequence_beforemove", "Not Set")
        self.input_sequence_aftermove = os.environ.get(prefix+"_sequence_aftermove", "Not Set")
        self.input_sequence_end = os.environ.get(prefix+"_sequence_end", "Not Set")
        self.input_save_meta_key = os.environ.get(prefix+"_save_meta_key", "")
        self.input_save_meta_value = os.environ.get(prefix+"_save_meta_value", "")
        self.input_debug = os.environ.get(prefix+"_debug", 1)

        log(self.input_pointname, message_type='debug', title=self.farmwarename)
        log(self.input_openfarm_slug, message_type='debug', title=self.farmwarename)
        log(self.input_age_min_day, message_type='debug', title=self.farmwarename)
        log(self.input_age_max_day, message_type='debug', title=self.farmwarename)
        log(self.input_filter_meta_key, message_type='debug', title=self.farmwarename)
        log(self.input_filter_meta_value, message_type='debug', title=self.farmwarename)
        log(self.input_sequence_init, message_type='debug', title=self.farmwarename)
        log(self.input_sequence_beforemove, message_type='debug', title=self.farmwarename)
        log(self.input_sequence_aftermove, message_type='debug', title=self.farmwarename)
        log(self.input_sequence_end, message_type='debug', title=self.farmwarename)
        log(self.input_save_meta_key, message_type='debug', title=self.farmwarename)
        log(self.input_save_meta_value, message_type='debug', title=self.farmwarename)
        log(self.input_debug, message_type='debug', title=self.farmwarename)
        
    def __init__(self,farmwarename):
        self.farmwarename = farmwarename
        self.get_input_env()
        self.api = API(self)
        self.points = {}

    def load_points_with_filters(self):
        self.points = Filter_Points(
            self.api.api_get('points'),
            name=self.input_pointname,
            openfarm_slug=self.input_openfarm_slug,
            age_min_day=self.input_age_min_day,
            age_max_day=self.input_age_max_day,
            meta_key=self.input_filter_meta_key,
            meta_value=self.input_filter_meta_value,
            pointer_type='Plant')

    def sort_points(self):
        #self.points = self.points ########## add sort opt_points,tab_id = Get_Optimal_Way(app_points)
        #self.points, self.tab_id = Get_Optimal_Way(self.points)
        pass

    def run(self):
        self.load_points_with_filters()
        self.sort_points()

        log(self.points,message_type='debug',title=self.farmwarename + ' : run')