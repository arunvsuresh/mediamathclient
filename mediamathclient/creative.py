import json
import requests
import os
import terminalone
import itertools


# connect to t1
def get_connection():
    creds = {
        "username": os.environ['MM_USERNAME'],
        "password": os.environ['MM_PASSWORD'],
        "api_key": os.environ['MM_API_KEY']
    }
    return terminalone.T1(auth_method="cookie", **creds)


class Creative:
    t1 = get_connection()

    headers = {'Content-Type': 'application/x-www-form-urlencoded', 'Accept': 'application/vnd.mediamath.v1+json',
               'Cookie': 'adama_session=' + str(t1.session_id)}

    def generate_url(self, obj_type):
        if obj_type == "atomic_creatives":
            service_url = self.t1._get_service_path('atomic_creatives') + "/"
            constructed_url = self.t1._construct_url("atomic_creatives", entity=None, child=None, limit=None)[0]
        elif obj_type == "strategy_concepts":
            service_url = self.t1._get_service_path('strategy_concepts') + "/"
            constructed_url = self.t1._construct_url("strategy_concepts", entity=None, child=None, limit=None)[0]

        elif obj_type == "strategies":
            service_url = self.t1._get_service_path('strategies') + "/"
            constructed_url = self.t1._construct_url("strategies", entity=None, child=None, limit=None)[0]

        base_url = "https://" + self.t1.api_base + "/"
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

        else:
            response_json['data'] = json_dict['data']
            response_json['msg_type'] = 'success'
            response_json['msg'] = ''

        return response_json

    def get_creative_by_id(self, creative_id):
        url = self.generate_url("atomic_creatives")
        url = url + "/" + str(creative_id) + "/?full=*"
        response = requests.get(url, headers=self.headers)
        json_dict = response.json()
        request_body = url, self.headers
        response_json = self.generate_json_response(json_dict, response, request_body)
        return json.dumps(response_json)

    def get_creatives_by_lineitem(self, lineitem_id):
        strategy_url = self.generate_url("strategies") + "/" + str(lineitem_id) + "/concepts"
        response = requests.get(strategy_url, headers=self.headers)
        request_body = strategy_url, self.headers
        json_dict = response.json()
        if 'errors' in json_dict:
            response_json = self.generate_json_response(json_dict, response, request_body)
            return json.dumps(response_json)
        elif len(json_dict['data']) == 0:
            response_json = self.generate_json_response(json_dict, response, request_body)
            return json.dumps(response_json)
        else:
            concept_ids = [concept['id'] for concept in json_dict['data']]
            json_dict, response = self.get_creatives_by_concept(concept_ids)
            response_json = self.generate_json_response(json_dict, response, request_body)
            return json.dumps(response_json)

    def get_creatives_by_concept(self, concept_ids):
        creative_response = []
        json_dict = {}
        errors = []
        for concept_id in concept_ids:
            concept_id = int(concept_id)
            # create url for each concept id
            creative_url = self.generate_url("atomic_creatives") + "/limit/concept={0}?full=*".format(str(concept_id))
            response = requests.get(creative_url, headers=self.headers)
            if 'errors' in response.json():
                errors.append(response.json()['errors'][0])
            else:
                creative_response.append(response.json()['data'])

        # if errors exist within creative calls
        if len(errors) >= 1:
            json_dict['errors'] = errors

        else:
            # flatten multi-dim array
            creative_response = list(itertools.chain.from_iterable(creative_response))
            json_dict['data'] = creative_response
        return json_dict, response
