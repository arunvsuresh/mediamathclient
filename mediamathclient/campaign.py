import json
import requests
import os
import terminalone
import xmltodict

class Campaign:

  def get_connection(self):
    creds = {
      "username": os.environ['MM_USERNAME'],
      "password": os.environ['MM_PASSWORD'],
      "api_key": os.environ['MM_API_KEY']
    }
    return terminalone.T1(auth_method="cookie", **creds)

  def generate_json_response(self, obj_type, json_dict, response, request_body):
    response_json = {
      "response_code": response.status_code,
      "request_body": request_body
    }

    # error checking
    if 'errors' in json_dict['result']:
      response_json['msg_type'] = 'error'
      response_json['msg'] = json_dict['result']['error']
      response_json['data'] = json_dict['result']['error']

    else:
      response_json['msg_type'] = 'success'
      response_json['msg'] = ''

      if obj_type == 'campaigns':

        response_json['data'] = json_dict['result']['entities']['entity']

      if obj_type == 'campaign':
        response_json['data'] = json_dict['result']['entity']['prop']

    return response_json

  def get_campaigns_by_advertiser(self, advertiser_id):
    t1 = self.get_connection()
    url = t1._construct_url("campaigns", entity=None, child=None, limit={"advertiser": int(advertiser_id)})[0]
    url = "https://" + t1.api_base + "/" + t1._get_service_path('campaigns') + "/" + url
    response = t1.session.get(url)
    # convert headers to real dict since it comes back as CaseInsensitiveDict
    headers = dict(response.headers)
    # get response content, comes back as xml
    xml_string = response.content
    # convert xml to json string and remove unwanted "@" symbol
    json_string = json.dumps(xmltodict.parse(xml_string), indent=4).replace(chr(64), '')
    # convert json string back to json dict to create proper json response
    json_dict = json.loads(json_string)
    request_body = url, headers
    response_json = self.generate_json_response("campaigns", json_dict, response, request_body)
    return json.dumps(response_json)

  def get_campaign_by_id(self, campaign_id):
    t1 = self.get_connection()
    url = t1._construct_url("campaigns", entity=campaign_id, child=None, limit=None)[0]
    url = "https://" + t1.api_base + "/" + t1._get_service_path('campaigns') + "/" + url
    response = t1.session.get(url)
    # convert headers to real dict since it comes back as CaseInsensitiveDict
    headers = dict(response.headers)
    # get response content, comes back as xml
    xml_string = response.content
    # convert xml to json string and remove unwanted "@" symbol
    json_string = json.dumps(xmltodict.parse(xml_string), indent=4).replace(chr(64), '')
    # convert json string back to json dict to create proper json response
    json_dict = json.loads(json_string)
    request_body = url, headers
    response_json = self.generate_json_response("campaign", json_dict, response, request_body)
    return json.dumps(response_json)