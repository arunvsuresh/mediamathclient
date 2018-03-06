import json
import requests
import os
import terminalone
import datetime


class DateException(Exception):
  pass


# connect to t1
def get_connection():
  creds = {
    "username": os.environ['MM_USERNAME'],
    "password": os.environ['MM_PASSWORD'],
    "api_key": os.environ['MM_API_KEY']
  }
  return terminalone.T1(auth_method="cookie", **creds)

class Campaign:

  t1 = get_connection()
  base_url = "https://" + t1.api_base + "/"
  service_url = t1._get_service_path('campaigns') + "/"
  constructed_url = t1._construct_url("campaigns", entity=None, child=None, limit=None)[0]
  url = base_url + service_url + constructed_url
  headers = {'Content-Type': 'application/x-www-form-urlencoded', 'Accept': 'application/vnd.mediamath.v1+json',
             'Cookie': 'adama_session=' + str(t1.session_id)}


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
    url = self.url + "/" + str(campaign_id)
    response = requests.get(url, headers=self.headers)
    json_dict = response.json()
    request_body = url, self.headers
    response_json = self.generate_json_response("campaign", json_dict, response, request_body)
    return json.dumps(response_json)

  def get_campaigns_by_advertiser(self, advertiser_id):
    url = self.url + "/limit/advertiser={0}".format(advertiser_id)
    response = requests.get(url, headers=self.headers)
    json_dict = response.json()
    request_body = url, self.headers
    response_json = self.generate_json_response("campaigns", json_dict, response, request_body)
    return json.dumps(response_json)

  def create_campaign(self, payload):
    url = self.url
    response = requests.post(url, headers=self.headers, data=payload)
    json_dict = response.json()
    request_body = url, self.headers
    response_json = self.generate_json_response("campaigns", json_dict, response, request_body)
    return json.dumps(response_json)

  # updates existing campaigns
  def save(self, payload, campaign_id):
    campaign = self.t1.get('campaigns', campaign_id, include="advertiser")
    if 'start_date' and 'end_date' in payload:
      payload['start_date'] = self.normalize_date_time(payload['start_date'])
      payload['end_date'] = self.normalize_date_time(payload['end_date'])
    campaign.save(data=payload)
    return campaign

  def normalize_date_time(self, date, date_format='%Y-%m-%dT%H:%M:%S'):
    """
      convert datetime str to datetime obj, since MM handles datetime obj --> str conversion on their end
      only needed for update(), not for create
    """
    date = datetime.datetime.strptime(date, date_format)
    return date


