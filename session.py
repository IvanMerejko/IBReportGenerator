import json
import requests
import logging
import pathlib
import urllib3
from typing import Dict
from urllib3.exceptions import InsecureRequestWarning
from fake_useragent import UserAgent

urllib3.disable_warnings(category=InsecureRequestWarning)

class InteractiveBrokersSession():

    def __init__(self):
        log_format = '%(asctime)-15s|%(filename)s|%(message)s'
        self.resource_url = "https://localhost:5000/v1"

        if not pathlib.Path('logs').exists():
            pathlib.Path('logs').mkdir()
            pathlib.Path('logs/log_file_custom.log').touch()

        logging.basicConfig(
            filename="logs/log_file_custom.log",
            level=logging.INFO,
            encoding="utf-8",
            format=log_format
        )

    def build_headers(self) -> Dict:
        # Fake the headers.
        headers = {
            "Content-Type": "application/json",
            "User-Agent": UserAgent().edge
        }

        return headers

    def build_url(self, endpoint: str) -> str:
        url = self.resource_url + endpoint

        return url

    def make_request(self, method: str, endpoint: str, params: dict = None, json_payload: dict = None) -> Dict:

        # Build the URL.
        url = self.build_url(endpoint=endpoint)
        headers = self.build_headers()

        logging.info(
            msg="------------------------"
        )

        logging.info(
            msg=f"JSON Payload: {json_payload}"
        )

        logging.info(
            msg=f"Request Method: {method}"
        )

        # Make the request.
        if method == 'post':
            response = requests.post(url=url, params=params, json=json_payload, verify=False, headers=headers)
        elif method == 'get':
            response = requests.get(url=url, params=params, json=json_payload, verify=False, headers=headers)
        elif method == 'delete':
            response = requests.delete(url=url, params=params, json=json_payload, verify=False, headers=headers)

        logging.info(
            msg="URL: {url}".format(url=url)
        )

        logging.info(
            msg=f'Response Status Code: {response.status_code}'
        )

        logging.info(
            msg=f'Response Content: {response.text}'
        )

        # If it's okay and no details.
        if response.ok and len(response.content) > 0:

            return response.json()

        elif len(response.content) > 0 and response.ok:

            return {
                'message': 'response successful',
                'status_code': response.status_code
            }

        elif not response.ok and endpoint =='/api/iserver/account':
            return response.json()

        elif not response.ok:

            if len(response.content) == 0:
                response_data = ''
            else:
                try:
                    response_data = response.json()
                except:
                    response_data = {'content': response.text}

            # Define the error dict.
            error_dict = {
                'error_code': response.status_code,
                'response_url': response.url,
                'response_body': response_data,
                'response_request': dict(response.request.headers),
                'response_method': response.request.method,
            }

            # Log the error.
            logging.error(
                msg=json.dumps(obj=error_dict, indent=4)
            )

            raise requests.HTTPError()