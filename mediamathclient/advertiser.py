import json
import requests
import os
import terminalone
import datetime


# connect to t1
def get_connection():
    creds = {
        "username": os.environ['MM_USERNAME'],
        "password": os.environ['MM_PASSWORD'],
        "api_key": os.environ['MM_API_KEY']
    }
    return terminalone.T1(auth_method="cookie", **creds)


class Advertiser:
    t1 = get_connection()
    base_url = "https://" + t1.api_base + "/"
    service_url = t1._get_service_path('advertisers') + "/"
    constructed_url = t1._construct_url("advertisers", entity=None, child=None, limit=None)[0]
    url = base_url + service_url + constructed_url
    headers = {'Content-Type': 'application/x-www-form-urlencoded', 'Accept': 'application/vnd.mediamath.v1+json',
               'Cookie': 'adama_session=' + str(t1.session_id)}

    def __init__(self, data=None, omg_advertiser=None):

        self.data = data
        self.omg_advertiser = omg_advertiser

    def generate_json_response(self, json_dict, response, request_body):
        response_json = {
            "response_code": response.status_code,
            "request_body": request_body
        }

        # error checking
        if 'errors' in json_dict:
            response_json['msg_type'] = 'error'
            response_json['msg'] = json_dict['errors']
            response_json['data'] = json_dict['errors']

        else:
            response_json['data'] = json_dict['data']
            response_json['msg_type'] = 'success'
            response_json['msg'] = ''

        return response_json

    def generate_url(self):
        base_url = "https://" + self.t1.api_base + "/"
        service_url = self.t1._get_service_path('advertisers') + "/"
        constructed_url = self.t1._construct_url("advertisers", entity=None, child=None, limit=None)[0]
        url = base_url + service_url + constructed_url
        return url

    def get_all(self):
        advertiser_id = int(advertiser_id)
        url = self.generate_url() + "/" + str(advertiser_id)
        return self.call_mm_api('GET', url)

    def call_mm_api(self, obj_type, url, data=None):
        if obj_type == 'GET':
            response = requests.get(url, headers=self.headers)
            json_dict = response.json()
            request_body = url, self.headers
            response_json = self.generate_json_response(json_dict, response, request_body)
            return json.dumps(response_json)

        if obj_type == 'POST':
            response = requests.post(url, headers=self.headers, data=data)
            json_dict = response.json()
            request_body = url, self.headers
            response_json = self.generate_json_response(json_dict, response, request_body)
            return json.dumps(response_json)
