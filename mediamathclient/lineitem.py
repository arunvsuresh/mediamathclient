import json
import requests
import os
import terminalone
import xmltodict
import datetime

def get_connection():
  creds = {
    "username": os.environ['MM_USERNAME'],
    "password": os.environ['MM_PASSWORD'],
    "api_key": os.environ['MM_API_KEY']
  }
  return terminalone.T1(auth_method="cookie", **creds)

class LineItem:

  t1 = get_connection()
  base_url = "https://" + t1.api_base + "/"
  service_url = t1._get_service_path('strategies') + "/"
  constructed_url = t1._construct_url("strategies", entity=None, child=None, limit=None)[0]
  url = base_url + service_url + constructed_url
  headers = {'Content-Type': 'application/x-www-form-urlencoded', 'Accept': 'application/vnd.mediamath.v1+json',
             'Cookie': 'adama_session=' + str(t1.session_id)}


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
      response_json['data'] = json_dict['data']
      response_json['msg_type'] = 'success'
      response_json['msg'] = ''

    return response_json

  def get_lineitem_by_id(self, lineitem_id):
    url = self.url + "/" + str(lineitem_id)
    response = requests.get(url, headers=self.headers)
    json_dict = response.json()
    request_body = url, self.headers
    response_json = self.generate_json_response(json_dict, response, request_body)
    return json.dumps(response_json)

  def get_lineitems_by_campaign(self, campaign_id):
    url = self.url + "/limit/campaign={0}".format(campaign_id)
    response = requests.get(url, headers=self.headers)
    json_dict = response.json()
    request_body = url, self.headers
    response_json = self.generate_json_response(json_dict, response, request_body)
    return json.dumps(response_json)

  def create_lineitem(self, payload):
    url = self.url
    response = requests.post(url, headers=self.headers, data=payload)
    json_dict = response.json()
    request_body = url, self.headers
    response_json = self.generate_json_response(json_dict, response, request_body)
    return json.dumps(response_json)

  # updates existing line items
  def save(self, payload, lineitem_id):
    line_item = self.t1.get('strategies', lineitem_id, include="campaign")
    if 'start_date' and 'end_date' in payload:
      payload['start_date'] = self.normalize_date_time(payload['start_date'])
      payload['end_date'] = self.normalize_date_time(payload['end_date'])
    line_item.save(data=payload)
    return line_item

  def normalize_date_time(self, date, date_format='%Y-%m-%dT%H:%M:%S'):
    """
      convert datetime str to datetime obj, since MM handles datetime obj --> str conversion on their end
      only needed for update(), not for create
    """
    date = datetime.datetime.strptime(date, date_format)
    return date