import requests
from requests.auth import HTTPBasicAuth
from rest_framework import status


def get_api_response(url, username, password):
    """
    We continuously hit api until we get response.
    
    TODO: we can add maximum number of tries and we can store a result in cache 
    to show recent response in case of failure
    """
    while True:
        try:
            api_response = requests.get(
                url,
                auth=HTTPBasicAuth(username, password),
                timeout=4,
            )
            if status.is_success(api_response.status_code):
                return api_response
        except requests.exceptions.RequestException as e:
            print('Got some Issue. Trying Again...')
            continue
