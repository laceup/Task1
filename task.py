import requests
import json
import csv

# This is the url to which the query is made
url = "https://data.fibrin29.hasura-app.io/v1/query"

# converting csv to json
csvfile = open('sample.csv', 'r')
#jsonfile = open('file.json', 'w')
field=("Date","AvgTemp","AvgTempUncertainity","City","Country","Latitude","Longitude")
reader = csv.DictReader(csvfile, field)
out = json.dumps( [ row for row in reader ] )
jout= json.loads(out)
#jsonfile.write(out)
# This is the json payload for the query
counter=0
objects = []
for row in jout:
    counter+=1
    objects.append(row)
    #if counter%10 == 0:
    requestPayload = {
    "type": "insert",
    "args": {
    "table": "temp_by_city",
    "objects": objects
    }
    }
    requests.post('https://data.fibrin29.hasura-app.io/v1/query', json=requestPayload)
    objects=[]
    # # Setting headers
    # headers = {
    #     "Content-Type": "application/json"
    # }
    #
    # # Make the query and store response in resp
    # resp = requests.request("POST", url, data=json.dumps(requestPayload), headers=headers)
    #
    # # resp.content contains the json response.
    # print(resp.content)
