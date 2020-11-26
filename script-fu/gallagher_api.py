import boto3
import urllib3
import json

QUERY = '?top=1000&fields=defaults,pdf_16337,lastSuccessfulAccessTime,status,cards'    
ROOT ='/api'        


class GallagherConnection(object):

    def __init__(self, API_Url = None, AuthorizationKey = None):
        self._endpoint=API_Url
        self._https=None
        self._baseUrl=None
        self._authorizationKey=  AuthorizationKey
        self.connect()
    
    def connect(self):        
        self._https=self.getHttpsEndpoint()
        self._baseUrl=self.cardHolderRootRESTUrl()        

    def getHttpsEndpoint(self):
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        https=urllib3.PoolManager(cert_reqs='CERT_NONE')    
        return https

    def getAuthenticationHeader(self):
        header = {'Authorization': self._authorizationKey }
        return header

    def cardHolderRootRESTUrl(self):    
        FEATURES='features'
        CARDHOLDERS='cardholders'
        HREF='href'       

        r = self._https.request('GET',self._endpoint+ROOT,headers = self.getAuthenticationHeader())        
        response= r.data.decode('utf-8')
        data=json.loads(response)
        url=data[FEATURES][CARDHOLDERS][CARDHOLDERS][HREF]        
        return url

    
    def getStatus(self,item):
        cards=item.get('cards')
        if cards is None : return 'No Card' 
        
        status='inactive'   
        for card in cards:          
            st=card['status']
            #if st['type'] != 'inactive' :  TBD  issueLevel
            status=st['type']
        
        return status

    def union(self,data):    
        coll={}
        for item in data['results']:  
            sapid=item.get('@SAP Personnel Number')             
            row = {
                'id' : item["id"],
                'firstName' : item.get('firstName'), 
                'lastName' : item.get('lastName'),
                'authorised' :  item.get('authorised'),
                'lastAccessTime' :  item.get('lastSuccessfulAccessTime'),
                'status' : self.getStatus(item)
            }        
            coll[sapid]=row
        
        return coll
        

    def getPhoto(self,id):

        url = "{}/{}".format(self._baseUrl,id)        
        r = self._https.request('GET',url,headers = self.getAuthenticationHeader())
        response= r.data.decode('utf-8')
        data=json.loads(response)

        ph=data.get('@ID Photo')
        if ph == "Not captured":  return None

        photoUrl=data['@ID Photo']['href']
        r = self._https.request('GET',photoUrl,headers = self.getAuthenticationHeader())                    
        return r.data
        

    def getGallagherCardholders(self):
        
        count=0
        url=self._baseUrl+QUERY
        full_db={}     

        while url is not None:            
            r = self._https.request('GET',url,headers = self.getAuthenticationHeader())
            response= r.data.decode('utf-8')
            
            data=json.loads(response)           
            thou=self.union(data)            
            full_db.update(thou)                        
 
            next = data.get("next")         
            url = next["href"] if next is not None else None       
                
            count+=1
            print("------------------------")
            print("1000 Loop # {0}".format(count))
            print("------------------------")

        return full_db