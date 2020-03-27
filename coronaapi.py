import requests

BASE_URL = "https://api.covid19api.com"

COUNTRIES_ENDPOINT = "/countries"
SUMMARY_ENDPOINT = "/summary"
CONFIRMED_ENDPOINT = "/total/country/{country}/status/confirmed"
RECOVERED_ENDPOINT = "/total/country/{country}/status/recovered"
DEATHS_ENDPOINT = "/total/country/{country}/status/deaths"

def fetch_countries():
    """
    Returns a list of all countries.
    """

    country_data = make_request(COUNTRIES_ENDPOINT)

    try:
        countries = ""
        
        for c in country_data:
            countries += c["Slug"] + ","

        return countries[:-1]
    except:
        return country_data 

def build_url(endpoint):
    """
    Build the final request URL for an endpoint.
    """
    
    if not endpoint:
        return None

    return BASE_URL + endpoint

def make_request(url, parameters = None):
    """
    Performs a request to the API, handling errors in the process.
    """
    try:
        r = requests.get(url = build_url(url), params = parameters)
    except:
        return "Error: Failed to retrieve data."

    try:
        data = r.json()
    except:
        return "Error: Retrieved unexpected data."

    return data

COUNTRY_DATA = fetch_countries()


def assert_country(country):
    """
    Asserts that the country provided is valid, meaning it is among the country slugs provided by the API. 
    """
    
    valid = False

    for c in COUNTRY_DATA.split(','):
        if c == country:
            valid = True
            break
    
    return valid

def fetch_summary():
    """
    Returns a summary of the data.
    """

    return make_request(SUMMARY_ENDPOINT) 

def fetch_confirmed(country):
    """
    Returns the total confirmed cases of a country. 
    """
    if(assert_country(country)):
        return make_request(CONFIRMED_ENDPOINT.format(country=country))

    return "Error: Invalid Country"
def fetch_recovered(country):
    """
    Returns the total recovered cases of a country. 
    """
    if(assert_country(country)):
        return make_request(RECOVERED_ENDPOINT.format(country=country))
    return "Error: Invalid Country"

def fetch_deaths(country):
    """
    Returns the total death cases of a country. 
    """
    if(assert_country(country)):
        return make_request(DEATHS_ENDPOINT.format(country=country))
    return "Error: Invalid Country"