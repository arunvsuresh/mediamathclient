from unittest import TestCase
from mediamathclient.mediamathclient import campaign
import os
import json

class TestMediaMathCampaign(TestCase):

  def test_connection(self):
    c = campaign.get_connection()
    session_id = c.session_id
    self.assertIsNotNone(session_id)

  def test_get_campaigns_by_advertiser(self):
    c = campaign.Campaign()
    campaigns = c.get_campaigns_by_advertiser(100429)
    self.assertIn('"msg_type": "success"', campaigns)

  def test_get_campaign_by_id(self):
    c = campaign.Campaign()
    c = c.get_campaign_by_id(482846)
    self.assertIn('"msg_type": "success"', c)

  def test_create_campaign(self):
    c = campaign.Campaign()

    data = {
      'ad_server_id': '9',
      'advertiser_id': 162259,
      'end_date': '2018-03-10',
      'goal_type': 'spend',
      'goal_value': '0.0001',
      'name': 'arun test campaign!!!',
      'service_type': 'SELF',
      'start_date': '2018-03-01',
      'total_budget': 2
    }

    new_campaign = c.create_campaign(data)
    self.assertIn('"msg_type": "success"', new_campaign)