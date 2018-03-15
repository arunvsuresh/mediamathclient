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

class LineItem:

  t1 = get_connection()
  headers = {'Content-Type': 'application/x-www-form-urlencoded', 'Accept': 'application/vnd.mediamath.v1+json',
             'Cookie': 'adama_session=' + str(t1.session_id)}

  def generate_url(self, obj_type):

    base_url = "https://" + self.t1.api_base + "/"

    if obj_type == "strategies":
      service_url = self.t1._get_service_path('strategies') + "/"
      constructed_url = self.t1._construct_url("strategies", entity=None, child=None, limit=None)[0]
      url = base_url + service_url + constructed_url
      return url

    elif obj_type == "deals":
      service_url = self.t1._get_service_path('deals') + "/"
      constructed_url = self.t1._construct_url("deals", entity=None, child=None, limit=None)[0]
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

  def get_lineitem_by_id(self, lineitem_id):
    url = self.generate_url('strategies') + "/" + str(lineitem_id)
    return self.make_call(url, 'GET')

  def get_lineitems_by_campaign(self, campaign_id):
    campaign_id = int(campaign_id)
    url = self.generate_url('strategies') + "/limit/campaign={0}".format(str(campaign_id))
    return self.make_call(url, 'GET')

  def create_lineitem(self, payload):
    url = self.generate_url('strategies')
    return self.make_call(url, 'POST', payload)

  # updates existing line items
  def update_lineitem(self, payload, lineitem_id):
    url = self.generate_url('strategies') + "/" + str(lineitem_id)
    return self.make_call(url, 'POST', payload)

  def assign_sitelist_to_strategy(self, lineitem_id, sitelist_ids):
    url = self.generate_url('strategies') + "/" + str(lineitem_id) + "/site_lists"
    payload = {

    }
    for idx, sitelist_id in enumerate(sitelist_ids):
      index = 'site_lists.{0}.id'.format(str(idx + 1))
      assigned = 'site_lists.{0}.assigned'.format(str(idx + 1))
      payload[index] = sitelist_id
      payload[assigned] = int(True)

    return self.make_call(url, 'POST', payload)

  def remove_sitelist_from_strategy(self, lineitem_id, sitelist_ids):
    url = self.generate_url('strategies') + "/" + str(lineitem_id) + "/site_lists"
    payload = {

    }
    for idx, sitelist_id in enumerate(sitelist_ids):
      index = 'site_lists.{0}.id'.format(str(idx + 1))
      assigned = 'site_lists.{0}.assigned'.format(str(idx + 1))
      payload[index] = sitelist_id
      payload[assigned] = int(False)

    return self.make_call(url, 'POST', payload)

  def update_strategy_domain_restrictions(self, lineitem_id, domains):
    url = self.generate_url('strategies') + "/" + str(lineitem_id) + "/domain_restrictions"
    payload = {

    }

    for idx, domain in enumerate(domains):
      index_domain = 'domains.{0}.domain'.format(str(idx + 1))
      index_restriction = 'domains.{0}.restriction'.format(str(idx + 1))
      payload[index_domain] = domain
      payload[index_restriction] = "INCLUDE"

    return self.make_call(url, 'POST', payload)

  def set_deal_targeting_for_strategy(self, lineitem_id, deal_ids):
    url = self.generate_url('strategies') + "/" + str(lineitem_id) + "/deals"
    payload = {

    }
    for idx, deal in enumerate(deal_ids):
      index = 'deal.{0}.id'.format(str(idx + 1))
      payload[index] = str(deal)

    payload["all_pmp"] = 0
    payload["all_exchanges"] = 0

    return self.make_call(url, 'POST', payload)

  def set_strategy_exchanges(self, lineitem_id, exchange_ids):
    lineitem_id = int(lineitem_id)
    url = self.generate_url('strategies') + "/" + str(lineitem_id) + "/supplies"
    payload = {

    }
    for idx, exchange_id in enumerate(exchange_ids):
      index = 'supply_source.{0}.id'.format(str(idx + 1))
      payload[index] = str(exchange_id)

    payload["all_pmp"] = 0
    payload["all_exchanges"] = 0

    return self.make_call(url, 'POST', payload)

  def get_deals(self):

    # make an initial request to pull all deals so we get the initial page/total_count info
    url = self.generate_url('deals') + "/?full=*"
    initial_response = requests.get(url, headers=self.headers)
    request_body = url, self.headers
    if 'errors' in initial_response.json():
      response_json = self.generate_json_response(initial_response.json(), initial_response, request_body)
      return json.dumps(response_json)

    else:

      """
          iterate through each page with the step being the page_offset of 100
      """
      # get the url for the next page of records to pull from
      next_page_url = initial_response.json()['meta']['next_page']
      # get the total count of all deals
      total_count = initial_response.json()['meta']['total_count']
      page_data = []
      # set 100 as the step since you can only have 100 records per page
      for page_offset in range(0, total_count, 100):
        response = requests.get(next_page_url, headers=self.headers)
        page_data.append(response.json()['data'])
      page_data = list(itertools.chain.from_iterable(page_data))

      json_dict = {
        'data': page_data
      }

      response_json = self.generate_json_response(json_dict, initial_response, request_body)
      return json.dumps(response_json)

  def get_deals_by_advertiser(self, advertiser_id):

    # make an initial request to pull all deals with advertiser_id perms so we get the initial page/total_count info
    url = self.generate_url('deals') + "/?permissions.[advertiser_id]={0}".format([advertiser_id])
    initial_response = requests.get(url, headers=self.headers)
    request_body = url, self.headers
    if 'errors' in initial_response.json():
      response_json = self.generate_json_response(initial_response.json(), initial_response, request_body)
      return json.dumps(response_json)

    else:

      """
          iterate through each page with the step being the page_offset of 100
      """
      # get the url for the next page of records to pull from
      next_page_url = initial_response.json()['meta']['next_page']
      # get the total count of all deals
      total_count = initial_response.json()['meta']['total_count']

      page_data = []
      # set 100 as the step since you can only have 100 records per page
      for page_offset in range(0, total_count, 100):
        response = requests.get(next_page_url, headers=self.headers)
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

