import json
import re
from notification_config import NotificationConfig

class NotificationRule(object):

    def __init__(self,store,site):
        self._exclusions=store['notifications/exclusions']
        self._shutdown['notifications/shutdown']        
        self._config=NotificationConfig(store,site)           
                

    def evaluate(self,persons):
        
        # mgr = Site Manager
        # shut = Site Emergency Srvice Distribution List
        # emg = Site Shutown Distribution List
        
        mgr=self._config.SiteManager()['email']
        emg=self._config.EmergencyServices()['email']
        shut=self._config.ShudownDistributionList()
        second=self._config.SecondaryBreathTestLocation()

        # if shutdown in Position title
        person=persons['employee']
        
        jobTitle=person['jobTitle']
        if self.isShutdown(jobTitle): return [shut,emg],self._config.EmergencyServices['mobile']

        # if on exclusion list 
        if self.isOnExclusionList(jobTitle) :  return [mgr,emg],self._config.SiteManager['mobile']

        # will use supervisor emails

        supervisor=persons['supervisor']       
        return [supervisor['businessEmail'],emg],supervisor['mobile']
   
    def SecondaryLocation(self):
        return self._config.SecondaryBreathTestLocation()
           
    def isOnExclusionList(self,jobTitle):
        
        #TODO add as config   
        exclusions = self._exclusions

        array=exclusions.split(':')
        
        for exclusion in array:
            pattern = '.*?{}.*'.format(exclusion.lower())           
            result = re.match(pattern, jobTitle.lower())                     
            if result:                 
                return True
        return False


    def isShutdown(self,jobTitle):

        #TODO add as config   
        shut=self._shutdown 

        pattern = '.*?{}.*'.format(shut.lower())
        result = re.match(pattern, jobTitle.lower())
        return result is not None 
