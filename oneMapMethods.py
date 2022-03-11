import requests


def locationdet(location):
    location = location
    params = {
        'searchVal': location,
        'returnGeom': 'Y',
        'getAddrDetails': 'N',
        'pageNum': "1"
    }
    search = requests.get('https://developers.onemap.sg/commonapi/search', params, timeout=0.2)
    searchdata = search.json()
    locationdet=[]
    print(searchdata)

    locationdet.append(float(searchdata["results"][0]["LATITUDE"]))
    locationdet.append(float(searchdata["results"][0]["LONGITUDE"]))
    locationdet.append(str(searchdata["results"][0]["SEARCHVAL"]))
    #Returns Array [Latitude, Longitude, Location of Place]
    return locationdet
