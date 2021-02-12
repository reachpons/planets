import json
import logging
import os
from ssm_parameter_store import SSMParameterStore
from smtp_email_sender import STMPEmail
from notification_rule import NotificationRule


def getData():

    return { "Hedland" : { 
                    "SiteManager" : { 
                        "email" : "",
                        "mobile" : "" 
                    },
                    "EmergencyServices" : { 
                        "email" : "",
                        "mobile" : "" 
                    },
                    "ShudownEmailDistributionList" :"",
                    "SecondaryBreathTestLocation" :""
                },
                "Fortescue Centre" :  { 
                    "SiteManager" : { 
                        "email" : "ibunney@fmgl.com.au",
                        "mobile" : "043 9983596" 
                    },
                    "EmergencyServices" : { 
                        "email" : "ibunney@fmgl.com.au",
                        "mobile" : "043 9983596" 
                    },
                    "ShudownEmailDistributionList" : "AlcolizerRekognitionDev@fmgl.com.au",
                    "SecondaryBreathTestLocation" : "Level 1 Crib Stack B"
                },
                "(Unknown)" :  { 
                    "SiteManager" : { 
                        "email" : "",
                        "mobile" : "" 
                    },
                    "EmergencyServices" : { 
                        "email" : "",
                        "mobile" : "" 
                    },
                    "ShudownEmailDistributionList" :"",
                    "SecondaryBreathTestLocation" :""
                }
            }

def main():
   
    event= {
            "default": "Alcolizer Rekognition - this message can be ignored.",
            "surname" : "Bunney",
            "givenNames" : "Ian",
            "shift" :"Day",
            "department" :  "Technology & Automation",
            "supervisorSurname" : "Lewis",
            "supervisorGivenNames" : "Shelley",
            "datetime" : "3 Feburary 2021: 11:30AM",
            "alcolizer" :"310210335",
            "displayedResult" : "0.003 g/100Ml BAC",
            "company" :" Fortescue Metals Group",
            "site" : "Fortescue Centre",
            "location" : "Level 3 - Security Build desk",
            "secondaryLocation" : " Level Kitchen",
            "recipients" : {
                "email" : ["ibunney@fmgl.com.au"],
                "mobile" : "0439983596"       
            }            
    }

    hierarchy = 'dev' # os.environ['hierarchy']
    global store
    store=SSMParameterStore(Path='/alcolizer-rekognition/{}'.format(hierarchy) )           
    
    site=event['site']
    rule = NotificationRule(store,site)    
    recipients,mobileNo=rule.evaluate(event)


if __name__ == "__main__":
    main()
