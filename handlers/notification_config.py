import json

class NotificationConfig(object):

    def __init__(self,store,site):
        self._store =store
        self._site=site
        self._config = self.getSiteConfig()

    def getSiteConfig(self):
        result = self._store['notifications/config'] 
        config = json.loads(result)
        siteConfig=config[self._site]        
        return siteConfig

    def SiteManager(self):        
        return self._config['SiteManager']
    
    def EmergencyServices(self):
        return self._config['EmergencyServices']

    def ShudownDistributionList(self):
        return self._config['ShudownEmailDistributionList']

    def SecondaryBreathTestLocation(self):
        return self._config['SecondaryBreathTestLocation']

