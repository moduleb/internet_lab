import json
import os

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

session = requests.Session()
retry = Retry(connect=3, backoff_factor=0.5)
adapter = HTTPAdapter(max_retries=retry)
session.mount('http://', adapter)
session.mount('https://', adapter)



def request_func(method, username=None, password=None, email=None, token = None, endpoint=None):

    """URL"""
    # if endpoint:
    #     url = f"http://0.0.0.0:8000/users/{endpoint}"
    # else:
    #     url = f"http://0.0.0.0:8000/users/"

    if endpoint:
        url = f"http://internet_lab_app:8000/users/{endpoint}"
    else:
        url = f"http://internet_lab_app:8000/users/"

    """PAYLOAD"""
    payload_dict = {}
    if username:
        payload_dict['username'] = username
    if password:
        payload_dict['password'] = password
    if email:
        payload_dict['email'] = email

    payload = json.dumps(payload_dict)

    """HEADERS"""
    headers = {
        'Content-Type': 'application/json'
    }
    if token:
        headers['Authorization'] = token

    """REQUEST"""
    try:
        response = requests.request(method, url, headers=headers, data=payload)
    except requests.exceptions.ConnectionError:
        print("Connection error occurred")
        return
    return response

