import json
import requests
import os
import terminalone
import xmltodict


def get_connection():
  creds = {
    "username": os.environ['MM_USERNAME'],
    "password": os.environ['MM_PASSWORD'],
    "api_key": os.environ['MM_API_KEY']
  }
  return terminalone.T1(auth_method="cookie", **creds)

class Campaign:

  t1 = get_connection()

  def generate_json_response(self, obj_type, json_dict, response, request_body):
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
      if obj_type == 'campaigns':
        response_json['data'] = json_dict['data']

      if obj_type == 'campaign':
        response_json['data'] = json_dict['data']

      response_json['msg_type'] = 'success'
      response_json['msg'] = ''

    return response_json

  def get_campaign_by_id(self, campaign_id):
    url = self.t1._construct_url("campaigns", entity=campaign_id, child=None, limit=None)[0]
    url = "https://" + self.t1.api_base + "/" + self.t1._get_service_path('campaigns') + "/" + url
    headers = {'Content-Type': 'application/json', 'Accept': 'application/vnd.mediamath.v1+json', 'Cookie': 'adama_session=' + str(self.t1.session_id)}
    response = requests.get(url, headers=headers)
    json_dict = response.json()
    request_body = url, headers
    response_json = self.generate_json_response("campaign", json_dict, response, request_body)
    return json.dumps(response_json)

  def get_campaigns_by_advertiser(self, advertiser_id):
    url = self.t1._construct_url("campaigns", entity=None, child=None, limit={"advertiser": int(advertiser_id)})[0]
    url = "https://" + self.t1.api_base + "/" + self.t1._get_service_path('campaigns') + "/" + url
    headers = {'Content-Type': 'application/json', 'Accept': 'application/vnd.mediamath.v1+json', 'Cookie': 'adama_session=' + str(self.t1.session_id)}
    response = requests.get(url, headers=headers)
    json_dict = response.json()
    request_body = url, headers
    response_json = self.generate_json_response("campaigns", json_dict, response, request_body)
    return json.dumps(response_json)

  def create_campaign(self, payload):
    url = self.t1._construct_url("campaigns", entity=None, child=None, limit=None)[0]
    url = "https://" + self.t1.api_base + "/" + self.t1._get_service_path('campaigns') + "/" + url
    headers = {'Content-Type': 'application/json', 'Accept': 'application/vnd.mediamath.v1+json', 'Cookie': 'adama_session=' + str(self.t1.session_id)}
    response = requests.post(url, headers=headers, data=payload)
    json_dict = response.json()
    request_body = url, headers
    response_json = self.generate_json_response("campaigns", json_dict, response, request_body)
    return json.dumps(response_json)
