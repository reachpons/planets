import json
import re
from notification_config import NotificationConfig

class NotificationRule(object):

    def __init__(self,store,site):
        self._config=NotificationConfig(store,site)   
        self._secondLocation=None
        self._contact=None
             

    def evaluate(self,persons):
        
        # mgr = Site Manager
        # shut = Site Emergency Srvice Distribution List
        # emg = Site Shutown Distribution List

        mgr,emg,shut,second,contact=self._config.unpack()
        self._secondLocation=second
        self._contact=contact

        # if shutdown in Position title
        person=persons['employee']

        jobTitle=person['jobTitle']
        if self.isShutdown(jobTitle): return [shut,emg]

        # if on exclusion list 
        if self.isOnExclusionList(jobTitle) :  return [mgr,emg]

        # will use supervisor emails

        supervisor=persons['supervisor']
        return [supervisor['businessEmail'],emg]

    def secondaryLocation(self):
        return self._secondLocation
    
    def contact(self):
        return self._contact
        

    def isOnExclusionList(self,jobTitle):
        
        #TODO add as config   
        exclusions = 'Group Manager|Director|Chief Executive Officer|Chief Representative China|Chief General Counsel|Chief Operating Officer|Deputy Chief Executive Officer|Chief Financial Officer'

        array=exclusions.split(':')
        
        for exclusion in array:
            pattern = '.*?{}.*'.format(exclusion.lower())           
            result = re.match(pattern, jobTitle.lower())                     
            if result:                 
                return True
        return False


    def isShutdown(self,jobTitle):

        shut='Shutdown' #TODO add as config   

        pattern = '.*?{}.*'.format(shut.lower())
        result = re.match(pattern, jobTitle.lower())
        return result is not None 
