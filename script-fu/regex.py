import re
import codecs
import unicodedata

exclusions = u'Shutdown:Group:Director:Chief Executive Officer:Chief Representative China:Chief General Counsel:Chief Operating Officer:Deputy Chief Executive Officer:Chief Financial Officer'
#exclusions = 'Financial:Shutdown:Group:Director:Chief:Operating:extra'

fake='Adhoc Contractors:' \
'EGWME:' \
'IB Early Works:' \
'Downer:' \
'Construction:' \
'Logistics and Expediting:' \
'Rail Operations Hedland C:' \
'Rail Operations Mainline D:' \
'MLG:' \
'Contracts Ports & Pipes:' \
'Construction:' \
'International Logistics:' \
'Energy:' \
'Global Project Generation & Targeting:' \
'Chief Executive Officer:' \
'Legal:' \
'Exploration & Operations:' \
'Operations:' \
'Chief Financial Officer:' \
'Deputy CEO:' \
'Procurement:' \
'Shutdown Manager:' \
'Chief Financial Officer:' \
'Group Shutdown Engineer'

def readTitles(fileName):
    loop=[]
    with codecs.open(fileName,'r', encoding = 'utf-8') as f:
        loop=f.read().splitlines()
        
    return loop

def main():
    #positions=readTitles('utf8-positions.txt')

    positions=fake.split(':')
   
    for posy in positions:
        position=posy.lower()
        array=exclusions.split(':')
        for exclusion in array:
            pattern = '.*?{}.*'.format(exclusion.lower())
           
            result = re.match(pattern, position)
                        
            if result: 
            
                print( 'Match {} - #: {}'.format(posy,exclusion))

            

if __name__ == "__main__":
    main()

