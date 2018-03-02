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
    c = json.loads(campaigns)
    self.assertIn(c['msg_type'], 'success')

  def test_get_campaign_by_id(self):
    c = campaign.Campaign()
    c = c.get_campaign_by_id(482846)
    c = json.loads(c)
    self.assertIn(c['msg_type'], 'success')

  def test_create_campaign(self):
    c = campaign.Campaign()

    data = {
      'advertiser_id': 162259,
      'ad_server_id': 9,
      'end_date': '2018-03-10T09:00:00+0000',
      'goal_type': 'spend',
      'goal_value': '0.0001',
      'name': 'arun test campaign 03/04/2018',
      'service_type': 'SELF',
      'start_date': '2018-03-02T23:59:00+0000',
      'total_budget': 2
    }
    new_campaign = c.create_campaign(data)
    new_campaign = json.loads(new_campaign)
    self.assertIn(new_campaign['msg_type'], 'success')

  # test when missing required field (advertiser_id in this case)
  def test_error_in_create_campaign(self):
    c = campaign.Campaign()

    data = {
      'ad_server_id': 9,
      'end_date': '2018-03-10T09:00:00+0000',
      'goal_type': 'spend',
      'goal_value': '0.0001',
      'name': 'arun test campaign 03/02/2018',
      'service_type': 'SELF',
      'start_date': '2018-03-02T23:59:00+0000',
      'total_budget': 2
    }
    new_campaign = c.create_campaign(data)
    new_campaign = json.loads(new_campaign)
    self.assertIn(new_campaign['msg_type'], 'error')
