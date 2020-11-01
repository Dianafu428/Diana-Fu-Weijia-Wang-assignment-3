import urllib.request
import json
from pprint import pprint

# Useful URLs (you need to add the appropriate parameters for your requests)
# MAPQUEST_BASE_URL = "http://www.mapquestapi.com/geocoding/v1/address"
# MBTA_BASE_URL = "https://api-v3.mbta.com/stops"

# Your API KEYS (you need to use your own keys - very long random characters)
MAPQUEST_API_KEY = "FNYY1KYvN2gka0ccyTJm3AkAQXzoxqCG"
MBTA_API_KEY = "38baaaea564f4d4483a53cdec082def3"


def buildUrl(place_name):
    """
    Build the map URL.
    """
    params = urllib.parse.urlencode({"key": MAPQUEST_API_KEY, "location": place_name})
    url = "http://www.mapquestapi.com/geocoding/v1/address?%s" % params
    return url


def get_lat_long(res):
    """
    Extract the latitude and longitude from the JSON response
    See https://developer.mapquest.com/documentation/geocoding-api/address/get/
    for Mapquest Geocoding  API URL formatting requirements.
    """
    data = res["results"][0]["locations"][0]["displayLatLng"]
    return data["lat"], data["lng"]


def get_closed_stop(place_name):
    """
    Given a place name or address, return its longitude strings, and also
    return the nearest MBTA stop and whether it is wheelchair accessible.
    """

    url = buildUrl(place_name)
    f = urllib.request.urlopen(url)
    response_text = f.read().decode("utf-8")
    response_data = json.loads(response_text)
    # pprint(response_data)

    lat, lng = get_lat_long(response_data)

    # test for MBTA stop
    params = urllib.parse.urlencode(
        {
            "sort": "distance",
            "filter[latitude]": lat,
            "filter[longitude]": lng,
            "filter[radius]": 0.1,
        }
    )

    url = "https://api-v3.mbta.com/stops?%s" % params
    f = urllib.request.urlopen(url)
    response_text = f.read().decode("utf-8")
    response_data = json.loads(response_text)

    if len(response_data["data"]) == 0:
        return lat, lng, None, None

    print(response_data["data"][0])

    name = response_data["data"][0]["attributes"]["name"]
    wheelchair_boarding = response_data["data"][0]["attributes"]["wheelchair_boarding"]

    return lat, lng, name, wheelchair_boarding


def main():
    """
    You can test all the functions here
    """
    # print(lat)
    # print(lng)
    # pprint(response_data)
    # print(name)
    # print(wheelchair_boarding)
    pass


if __name__ == "__main__":
    main()
