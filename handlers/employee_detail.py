import json
from employee_api import EmployeeAPI

# this uses the SucessFactors API 

class EmployeeDetail(object):

    def __init__(self, SAPId):
        self._SAPId=SAPId 
    
    def getPhone(self,person):
        
        mobile=''
        if person.get('phone') :
            for ph in person['phone']:
                mobile=ph['number']
                break
        return mobile

    def getEmail(self,person):
            
        email=''
        if person.get('email') :
            for ph in person['email']:
                email=ph['address']
                break
        return email


    def fetch(self):                
  
        api = EmployeeAPI(self._SAPId)
        sf = api.getEmployeeAndSupervisor()

        employee={
             'firstName': sf['employee']['preferredName'],
             'surname': sf['employee']['lastName'],
             'department': sf['employee']['job']['department'],
             'jobTitle' : sf['employee']['job']['title'],
             'businessEmail' : self.getEmail(sf['employee']),
             'mobile':  self.getPhone(sf['employee'])
        }      
        supervisor={
             'firstName': sf['supervisor']['preferredName'],
             'surname': sf['supervisor']['lastName'],
             'department': sf['supervisor']['job']['department'],
             'jobTitle' : sf['supervisor']['job']['title'],
             'businessEmail' : self.getEmail(sf['supervisor']),
             'mobile':  self.getPhone(sf['supervisor'])
        }
        return {
                "employee": employee,
                "supervisor": supervisor            
        }