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

  def get_campaigns(self):
    response_json = {}
    t1 = self.get_connection()
    url = "https://" + t1.api_base + "/" + t1._get_service_path('campaigns') + "/campaigns"
    response = t1.session.get(url)
    # convert headers to real dict since it comes back as CaseInsensitiveDict
    headers = dict(response.headers)
    # get response content, comes back as xml
    xml_string = response.content
    # convert xml to json string and remove unwanted "@" symbol
    json_string = json.dumps(xmltodict.parse(xml_string), indent=4).replace(chr(64), '')
    # convert json string back to json dict to create proper json response
    json_dict = json.loads(json_string)
    # error checking
    if 'errors' in json_dict['result']:
      response_json['msg_type'] = 'error'
      response_json['msg'] = json_dict['result']['error']
      response_json['data'] = json_dict['result']['error']
      response_json['response_code'] = response.status_code
      response_json['request_body'] = url, response.headers

    else:
      response_json['msg_type'] = 'success'
      response_json['msg'] = ''
      response_json['data'] = json_dict['result']['entities']['entity']
      response_json['response_code'] = response.status_code
      response_json['request_body'] = url, headers

    return json.dumps(response_json)
