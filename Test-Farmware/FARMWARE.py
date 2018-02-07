import os
import datetime
from API import API
from CeleryPy import log
from CeleryPy import move_absolute
from CeleryPy import execute_sequence

class MyFarmware():

    def get_input_env(self):
        prefix = self.farmwarename.lower().replace('-','_')
        
        self.input_pointname = os.environ.get(prefix+"_pointname", "")
        self.input_openfarm_slug = os.environ.get(prefix+"_openfarm_slug", "")
        self.input_age_min_day = os.environ.get(prefix+"__age_min_day", 0)
        self.input_age_max_day = os.environ.get(prefix+"__age_max_day", 36500)
        self.input_filter_meta_key = os.environ.get(prefix+"_filter_meta_key", "")
        self.input_filter_meta_value = os.environ.get(prefix+"_filter_meta_value", "")
        self.input_sequence_init = os.environ.get(prefix+"_sequence_init", "Not Set")
        self.input_sequence_beforemove  = os.environ.get(prefix+"_sequence_beforemove", "Not Set")
        self.input_sequence_aftermove = os.environ.get(prefix+"_sequence_aftermove", "Not Set")
        self.input_sequence_end = os.environ.get(prefix+"_sequence_end", "Not Set")
        self.input_save_meta_key = os.environ.get(prefix+"_save_meta_key", "")
        self.input_save_meta_value = os.environ.get(prefix+"_save_meta_value", "")
        self.input_debug = os.environ.get(prefix+"_debug", 2)

        if self.input_debug >= 1:
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

    def apply_filters(self, points, point_name='', openfarm_slug='', age_min_day=0, age_max_day=36500, meta_key='', meta_value='', pointer_type='Plant'):
        filtered_points = []
        now = datetime.datetime.utcnow()
        for p in points:
            age_day = 1
            b_meta = False
            if str(age_min_day) != '' and str(age_max_day) != '':
                age_day = (now - datetime.datetime.strptime(p['created_at'], '%Y-%m-%dT%H:%M:%S.%fZ')).days
            if meta_key != '':
                try:
                    b_meta = ((p['meta'][meta_key]).lower() == meta_value.lower())
                except:
                    b_meta = False
            else:
                b_meta = True
            if p['pointer_type'].lower() == pointer_type.lower() and \
                (p['name'].lower() == point_name.lower() or point_name == '') and \
                (p['openfarm_slug'].lower() == openfarm_slug.lower() or openfarm_slug == '') and \
                (age_min_day <= age_day <= age_max_day) and \
                b_meta:
                #filtered_points.append(p.copy())
                filtered_points.append(p)
        return filtered_points

    def load_points_with_filters(self):
        self.points = self.apply_filters(
            points=self.api.api_get('points'),
            point_name=self.input_pointname,
            openfarm_slug=self.input_openfarm_slug,
            age_min_day=self.input_age_min_day,
            age_max_day=self.input_age_max_day,
            meta_key=self.input_filter_meta_key,
            meta_value=self.input_filter_meta_value,
            pointer_type='Plant')
        

    def sort_points(self):
        self.points = sorted(self.points , key=lambda elem: (int(elem['x']), int(elem['y'])))
        if self.input_debug >= 1: log(self.points, message_type='debug', title=str(self.farmwarename) + ' : run')
        #self.points, self.tab_id = Get_Optimal_Way(self.points)

    def load_sequences_id(self):
        self.sequences = self.api.api_get('sequences')
        self.input_sequence_init_id = -1
        self.input_sequence_beforemove_id = -1
        self.input_sequence_aftermove_id = -1
        self.input_sequence_end_id = -1
        for s in self.sequences:
            if str(s['name']).lower() == self.input_sequence_init.lower() : self.input_sequence_init_id = int(s['id'])
            if str(s['name']).lower() == self.input_sequence_beforemove.lower() : self.input_sequence_beforemove_id = int(s['id'])
            if str(s['name']).lower() == self.input_sequence_aftermove.lower() : self.input_sequence_aftermove_id = int(s['id'])    
            if str(s['name']).lower() == self.input_sequence_end.lower() : self.input_sequence_end_id = int(s['id'])    
        if self.input_debug >= 1:
            log('init: ' + self.input_sequence_init + ' id:' + str(self.input_sequence_init_id), message_type='debug', title=str(self.farmwarename) + ' : load_sequences_id')
            log('before: ' + self.input_sequence_beforemove + ' id:' + str(self.input_sequence_beforemove_id), message_type='debug', title=str(self.farmwarename) + ' : load_sequences_id')
            log('after: ' + self.input_sequence_aftermove + ' id:' + str(self.input_sequence_aftermove_id), message_type='debug', title=str(self.farmwarename) + ' : load_sequences_id')
            log('end: ' + self.input_sequence_end + ' id:' + str(self.input_sequence_end_id), message_type='debug', title=str(self.farmwarename) + ' : load_sequences_id')
    
    def execute_sequence_init(self):
        if self.input_sequence_init_id != -1 :
            if self.input_debug >= 1: log('Execute Sequence: ' + self.input_sequence_init + ' id:' + str(self.input_sequence_init_id), message_type='debug', title=str(self.farmwarename) + ' : execute_sequence_init')
            if self.input_debug < 2: execute_sequence(self.input_sequence_init_id)

    def execute_sequence_before(self):
        if self.input_sequence_beforemove_id != -1 : 
            if self.input_debug >= 1: log('Execute Sequence: ' + self.input_sequence_beforemove + ' id:' + str(self.input_sequence_beforemove_id), message_type='debug', title=str(self.farmwarename) + ' : execute_sequence_before')
            if self.input_debug < 2: execute_sequence(self.input_sequence_beforemove_id)
                

    def execute_sequence_after(self):
        if self.input_sequence_aftermove_id != -1 : 
            if self.input_debug >= 1: log('Execute Sequence: ' + self.input_sequence_aftermove + ' id:' + str(self.input_sequence_aftermove_id), message_type='debug', title=str(self.farmwarename) + ' : execute_sequence_after')
            if self.input_debug < 2: execute_sequence(self.input_sequence_aftermove_id)

    def execute_sequence_end(self):
        if self.input_sequence_end_id != -1 : 
            if self.input_debug >= 1: log('Execute Sequence: ' + self.input_sequence_end + ' id:' + str(self.input_sequence_end_id), message_type='debug', title=str(self.farmwarename) + ' : execute_sequence_end')
            if self.input_debug < 2: execute_sequence(self.input_sequence_end_id)

    def move_absolute_point(self,point):
            if self.input_debug >= 1: log('Move absolute: ' + str(point) , message_type='debug', title=str(self.farmwarename) + ' : move_absolute_point')
            if self.input_debug < 2: pass # move_absolute


    def loop_points(self):
        for p in self.points:
            self.execute_sequence_before()
            self.move_absolute_point(p)
            self.execute_sequence_after()
            
    
    def run(self):
        self.load_points_with_filters()
        self.sort_points()
        self.load_sequences_id()
        self.execute_sequence_init()        
        self.loop_points()
        self.execute_sequence_end()
        
