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

    def unpack(self):

        mgr=self._config['SiteManager']
        emg=self._config['EmergencyServicesDistributionList']
        shut=self._config['ShudownDistributionList']
        second=self._config['SecondaryBreathTestLocation']
        contact=self._config['ContactPhone']
        return mgr,emg,shut,second,contact
