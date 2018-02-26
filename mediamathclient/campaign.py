import json
import requests
import os
import terminalone

class Campaign:

  def get_connection(self):
    creds = {
      "username": os.environ['MM_USERNAME'],
      "password": os.environ['MM_PASSWORD'],
      "api_key": os.environ['MM_API_KEY']
    }
    return terminalone.T1(auth_method="cookie", **creds)
