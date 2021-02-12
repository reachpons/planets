import json
from ssm_parameter_store import SSMParameterStore
from locations import Location


def main():
        
    hierarchy = 'dev' # os.environ['hierarchy']
    global store
    store=SSMParameterStore(Path='/alcolizer-rekognition/{}'.format(hierarchy) )


    location= Location(store)
    results=location[int('33000581')]
   
    one = location.parse(results)
    print (one)
    results=location[int('44')]
    two = location.parse(results)
    print(two)


if __name__ == "__main__":    
    main()


