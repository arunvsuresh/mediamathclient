import json
import requests
import os
import terminalone
import itertools


def get_connection():
    creds = {
        "username": os.environ['MM_USERNAME'],
        "password": os.environ['MM_PASSWORD'],
        "api_key": os.environ['MM_API_KEY']
    }
    return terminalone.T1(auth_method="cookie", **creds)


class SupplySource:
    t1 = get_connection()
    headers = {'Content-Type': 'application/x-www-form-urlencoded', 'Accept': 'application/vnd.mediamath.v1+json',
               'Cookie': 'adama_session=' + str(t1.session_id)}
    page_limit = 100

    def generate_url(self, obj_type):

        base_url = "https://" + self.t1.api_base + "/"

        if obj_type == "supply_sources":
            service_url = self.t1._get_service_path('supply_sources') + "/"
            constructed_url = self.t1._construct_url("supply_sources", entity=None, child=None, limit=None)[0]
            url = base_url + service_url + constructed_url
            return url

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

        elif 'data' not in json_dict:
            response_json['data'] = json_dict
            response_json['msg_type'] = 'success'
            response_json['msg'] = ''

        else:
            response_json['data'] = json_dict['data']
            response_json['msg_type'] = 'success'
            response_json['msg'] = ''

        return response_json

    def get_supply_sources(self):
        url = self.generate_url("supply_sources")
        initial_response = requests.get(url, headers=self.headers)
        request_body = url, self.headers
        # calculate last page
        end = int(round(int(initial_response.json()['meta']['total_count']) / self.page_limit))
        page_data = []
        for i in range(-1, end):
            # offset is multiple of 100
            offset = (i + 1) * self.page_limit
            # use offset to get every page
            url = self.generate_url('supply_sources') + "/?page_offset={0}".format(offset)
            response = requests.get(url, headers=self.headers)
            page_data.append(response.json()['data'])
        page_data = list(itertools.chain.from_iterable(page_data))

        json_dict = {
            'data': page_data
        }

        response_json = self.generate_json_response(json_dict, initial_response, request_body)
        return json.dumps(response_json)

    def make_call(self, url, method_type, payload=None):

        if method_type == 'GET':
            response = requests.get(url, headers=self.headers, data=payload)
            json_dict = response.json()
            request_body = url, self.headers
            response_json = self.generate_json_response(json_dict, response, request_body)
            return json.dumps(response_json)

        if method_type == 'POST':
            response = requests.post(url, headers=self.headers, data=payload)
            json_dict = response.json()
            request_body = url, self.headers
            response_json = self.generate_json_response(json_dict, response, request_body)
            return json.dumps(response_json)
