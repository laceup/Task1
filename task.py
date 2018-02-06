import requests
import csv

url = "https://data.fibrin29.hasura-app.io/v1/query"
admin_token = ""
csv_filename = "GlobalLandTemperaturesByCity.csv"

headers = {
    "Content-Type": "application/json",
    "Authorization": "Bearer " + admin_token
}

# create object and bulkPayload arrays
objects = []
bulkPayload = []

# open the file without header
with open(csv_filename, 'r') as csvfile:
    # set header names
    field = ("Date", "AvgTemp", "AvgTempUncertainity", "City", "Country",
             "Latitude", "Longitude")
    # types of columns: ("Date", "Numeric:NULL", "Numeric:NULL", "Text:NULL", "Text:NULL",
    #                    "Text:NULL", "Text:NULL")
    # read the file
    reader = csv.DictReader(csvfile, field, quoting=csv.QUOTE_NONE)

    # set counters
    counter = 0
    last_inserted_row = 0

    # loop through the row
    for row in reader:
        # increment the counter
        counter += 1
        # if any column is empty, set it as None
        for key in row:
            if len(row[key]) == 0:
                row[key] = None
        # add row to objects
        objects.append(row)
        # when objects has 100 elements,
        if len(objects) == 100:
            # append objects to bulkPayload
            bulkPayload.append({
                "type": "insert",
                "args": {
                    "table": "temp_by_city",
                    "objects": objects
                }
            })
            # clear objects
            objects = []
        # when bulkPayload has 10 elements,
        if len(bulkPayload) == 10:
            # create the main payload
            mainPayload = {
                "type": "bulk",
                "args": bulkPayload
            }
            # print some output
            print("inserting rows from " +
                  str(last_inserted_row) + " to " + str(counter))
            # make the request
            resp = requests.post(url, json=mainPayload, headers=headers)
            # print the response
            print(resp.json())
            # reset bulkPayload
            bulkPayload = []
            # set last inserted to counter
            last_inserted_row = counter

            # continue loop
