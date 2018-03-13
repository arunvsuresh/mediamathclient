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

    elif 'data' not in json_dict:
      response_json['data'] = json_dict
      response_json['msg_type'] = 'success'
      response_json['msg'] = ''

    else:
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
  def update_lineitem(self, payload, lineitem_id):
    url = self.url + "/" + str(lineitem_id)
    response = requests.post(url, headers=self.headers, data=payload)
    json_dict = response.json()
    request_body = url, self.headers
    response_json = self.generate_json_response(json_dict, response, request_body)
    return json.dumps(response_json)

  def normalize_date_time(self, date, date_format='%Y-%m-%dT%H:%M:%S'):
    """
      convert datetime str to datetime obj, since MM handles datetime obj --> str conversion on their end
      only needed for update(), not for create
    """
    date = datetime.datetime.strptime(date, date_format)
    return date

  def assign_sitelist_to_strategy(self, lineitem_id, sitelist_ids):
    url = self.url + "/" + str(lineitem_id) + "/site_lists"
    payload = {

    }
    for idx, sitelist_id in enumerate(sitelist_ids):
      index = 'site_lists.{0}.id'.format(str(idx + 1))
      assigned = 'site_lists.{0}.assigned'.format(str(idx + 1))
      payload[index] = sitelist_id
      payload[assigned] = int(True)
    response = requests.post(url, headers=self.headers, data=payload)
    json_dict = response.json()
    request_body = url, self.headers
    response_json = self.generate_json_response(json_dict, response, request_body)
    return json.dumps(response_json)

  def update_strategy_domain_restrictions(self, lineitem_id, domains):
    url = self.url + "/" + str(lineitem_id) + "/domain_restrictions"
    payload = {

    }

    for idx, domain in enumerate(domains):
      index_domain = 'domains.{0}.domain'.format(str(idx + 1))
      index_restriction = 'domains.{0}.restriction'.format(str(idx + 1))
      payload[index_domain] = domain
      payload[index_restriction] = "INCLUDE"

    response = requests.post(url, headers=self.headers, data=payload)
    json_dict = response.json()
    request_body = url, self.headers
    response_json = self.generate_json_response(json_dict, response, request_body)
    return json.dumps(response_json)

  def set_deal_targeting_for_strategy(self, lineitem_id, deal_ids):
    url = self.url + "/" + str(lineitem_id) + "/deals"
    payload = {

    }
    for idx, deal in enumerate(deal_ids):
      index = 'deal.{0}.id'.format(str(idx + 1))
      payload[index] = str(deal)

    payload["all_pmp"] = 0
    payload["all_exchanges"] = 0

    response = requests.post(url, headers=self.headers, data=payload)
    json_dict = response.json()
    request_body = url, self.headers
    response_json = self.generate_json_response(json_dict, response, request_body)
    return json.dumps(response_json)

  def set_strategy_exchanges(self, lineitem_id, exchange_ids):
    url = self.url + "/" + str(lineitem_id) + "/supplies"
    payload = {

    }
    for idx, exchange_id in enumerate(exchange_ids):
      index = 'supply_source.{0}.id'.format(str(idx + 1))
      payload[index] = str(exchange_id)

    payload["all_pmp"] = 0
    payload["all_exchanges"] = 0

    response = requests.post(url, headers=self.headers, data=payload)
    json_dict = response.json()
    request_body = url, self.headers
    response_json = self.generate_json_response(json_dict, response, request_body)
    return json.dumps(response_json)
