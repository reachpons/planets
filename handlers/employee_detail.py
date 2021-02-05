import json


# this uses the SucessFactors API 

class EmployeeDetail(object):

    def __init__(self, APIEndpoint):
        self._server=APIEndpoint 
    
    def fetch(self,employeeID ):                
        # 'shift' :'Day'
       tmp={ 
            'employee' : {
                'employeeId' :'3445627',
                'firstName' : 'Ian Bruce',
                'surname' : 'Bunney',
                'jobTitle' : 'Cloud Architect',
                'businessEmail' :'ibunney@fmgl.com.au',
                'mobile': '0439983596',
                'department' : 'Technology & Automation'
            },
            'supervisor' : {
                'employeeId' : '345617',
                'surname' :'Lewis', 
                'firstName' :'Shelley',  
                'jobTitle' : 'Project Manager',                                          
                'businessEmail' :'shelewis@fmgl.com.au',
                'mobile': '0439983596',            
                'department' : 'Technology & Automation'
            }
       }

       return tmp
