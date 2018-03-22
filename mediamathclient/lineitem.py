import itertools
import json
import requests
from base import Base

class LineItem(Base):

  page_limit = 100

  obj_name = "strategies"

  # def generate_url(self, obj_type):
  #
  #   base_url = "https://" + self.t1.api_base + "/"
  #
  #   if obj_type == "strategies":
  #     service_url = self.t1._get_service_path('strategies') + "/"
  #     constructed_url = self.t1._construct_url("strategies", entity=None, child=None, limit=None)[0]
  #     url = base_url + service_url + constructed_url
  #     return url
  #
  #   elif obj_type == "deals":
  #     service_url = self.t1._get_service_path('deals') + "/"
  #     constructed_url = self.t1._construct_url("deals", entity=None, child=None, limit=None)[0]
  #     url = base_url + service_url + constructed_url
  #     return url

  # def generate_json_response(self, json_dict, response, request_body):
  #
  #   response_json = {
  #     "response_code": response.status_code,
  #     "request_body": request_body
  #   }
  #
  #   # error checking
  #   if 'errors' in json_dict:
  #     response_json['msg_type'] = 'error'
  #     response_json['msg'] = json_dict['errors']
  #     response_json['data'] = json_dict['errors']
  #
  #   elif 'data' not in json_dict:
  #     response_json['data'] = json_dict
  #     response_json['msg_type'] = 'success'
  #     response_json['msg'] = ''
  #
  #   else:
  #     response_json['data'] = json_dict['data']
  #     response_json['msg_type'] = 'success'
  #     response_json['msg'] = ''
  #
  #   return response_json

  def get_lineitems_by_campaign(self, campaign_id):
    campaign_id = int(campaign_id)
    url = self.generate_url() + "/limit/campaign={0}".format(str(campaign_id))
    return self.call_mm_api('GET', url)

  def assign_sitelist_to_strategy(self, lineitem_id, sitelist_ids):
    url = self.generate_url() + "/" + str(lineitem_id) + "/site_lists"
    payload = {

    }
    for idx, sitelist_id in enumerate(sitelist_ids):
      index = 'site_lists.{0}.id'.format(str(idx + 1))
      assigned = 'site_lists.{0}.assigned'.format(str(idx + 1))
      payload[index] = sitelist_id
      payload[assigned] = int(True)

    return self.call_mm_api('POST', url, payload)

  def remove_sitelist_from_strategy(self, lineitem_id, sitelist_ids):
    url = self.generate_url() + "/" + str(lineitem_id) + "/site_lists"
    payload = {

    }
    for idx, sitelist_id in enumerate(sitelist_ids):
      index = 'site_lists.{0}.id'.format(str(idx + 1))
      assigned = 'site_lists.{0}.assigned'.format(str(idx + 1))
      payload[index] = sitelist_id
      payload[assigned] = int(False)

    return self.call_mm_api('POST', url, payload)

  def update_strategy_domain_restrictions(self, lineitem_id, domains):
    url = self.generate_url() + "/" + str(lineitem_id) + "/domain_restrictions"
    payload = {

    }

    for idx, domain in enumerate(domains):
      index_domain = 'domains.{0}.domain'.format(str(idx + 1))
      index_restriction = 'domains.{0}.restriction'.format(str(idx + 1))
      payload[index_domain] = domain
      payload[index_restriction] = "INCLUDE"

    return self.call_mm_api('POST', url, payload)

  def set_deal_targeting_for_strategy(self, lineitem_id, deal_ids):
    url = self.generate_url() + "/" + str(lineitem_id) + "/deals"
    payload = {

    }
    for idx, deal in enumerate(deal_ids):
      index = 'deal.{0}.id'.format(str(idx + 1))
      payload[index] = str(deal)

    payload["all_pmp"] = 0
    payload["all_exchanges"] = 0

    return self.call_mm_api('POST', url, payload)

  def set_strategy_exchanges(self, lineitem_id, exchange_ids):
    lineitem_id = int(lineitem_id)
    url = self.generate_url() + "/" + str(lineitem_id) + "/supplies"
    payload = {

    }
    for idx, exchange_id in enumerate(exchange_ids):
      index = 'supply_source.{0}.id'.format(str(idx + 1))
      payload[index] = str(exchange_id)

    payload["all_pmp"] = 0
    payload["all_exchanges"] = 0

    return self.call_mm_api('POST', url, payload)

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
          iterate through each page with the page_offset being a multiple of 100 since page_limit is 100
      """

      # calculate last page
      end = int(round(int(initial_response.json()['meta']['total_count']) / self.page_limit))
      page_data = []
      for i in range(-1, end):
        # offset is multiple of 100
        offset = (i + 1) * self.page_limit
        # use offset to get every page
        url = self.generate_url('deals') + "/?page_offset={0}".format(offset)
        response = requests.get(url, headers=self.headers)
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
          iterate through each page with the page_offset being a multiple of 100 since page_limit is 100
      """
      end = int(round(int(initial_response.json()['meta']['total_count']) / self.page_limit)) + self.page_limit
      page_data = []
      for i in range(-1, end):
        # offset is multiple of 100
        offset = (i + 1) * self.page_limit
        # use offset to get every page
        url = self.generate_url('deals') + "/?page_offset={0}".format(offset)
        response = requests.get(url, headers=self.headers)
        page_data.append(response.json()['data'])
      page_data = list(itertools.chain.from_iterable(page_data))

      json_dict = {
        'data': page_data
      }

      response_json = self.generate_json_response(json_dict, initial_response, request_body)
      return json.dumps(response_json)
