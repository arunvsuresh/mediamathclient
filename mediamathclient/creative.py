import json
import requests
import os
import terminalone
import itertools
from base import Base

class Creative(Base):

  obj_name = "atomic_creatives"

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
