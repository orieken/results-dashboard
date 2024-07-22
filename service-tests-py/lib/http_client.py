import requests
import os
import logging


class HTTPClient:
    def __init__(self):
        self.session = requests.Session()
        self.setup_logger()

    def setup_logger(self):
        self.logger = logging.getLogger('HTTPClient')
        handler = logging.StreamHandler()
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)
        self.logger.setLevel(logging.INFO if os.getenv('VERBOSE', '0') == '0' else logging.DEBUG)

    def set_headers(self, headers):
        self.session.headers.update(headers)

    def post(self, url, data):
        self.logger.debug(f"POSTing to {url} with data {data} and headers {self.session.headers}")
        response = self.session.post(url, json=data)
        return response

    def get_response_info(self, response):
        return response.status_code, response.json()
