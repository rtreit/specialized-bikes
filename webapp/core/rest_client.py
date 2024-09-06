
import logging
import json
import requests

from django.utils import timezone

from .models import OutgoingRequest

logger = logging.getLogger("rest_client")
   
class RestClient:
    def __init__(self, headers={}):
        self.headers = headers or {}
    
    def get(self, url) -> requests.Response:
        return requests.get(url, headers=self.headers)
    
    def post(self, url, payload={}) -> requests.Response:
        return requests.post(url, json=payload, headers=self.headers)

    def patch(self, url, payload={}) -> requests.Response:
        return requests.patch(url, json=payload, headers=self.headers)

    def put(self, url, payload={}) -> requests.Response:
        return requests.put(url, json=payload, headers=self.headers)

    def delete(self, url) -> requests.Response:
        return requests.patch(url, headers=self.headers)

    def make_request(self, url: str, method: str, payload: dict = {}):
        logger.info(f"Making Request to {url} at {str(timezone.now())}")
        requestLog = OutgoingRequest(url=url, method=method, payload=json.dumps(payload))
        response = None
        if method.lower() == 'get':
            response = self.get(url)
        
        if method.lower() == 'post':
            response = self.post(url, payload)
        
        if method.lower() == 'put':
            response = self.put(url, payload)

        if method.lower() == 'patch':
            response = self.patch(url, payload)

        if method.lower() == 'delete':
            response = self.patch(url)

        requestLog.response = response.text
        requestLog.status_code = response.status_code
        requestLog.save()
        return response
        
       

        




            





