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
    print c
    self.assertIn(c['msg_type'], 'success')

  def test_get_campaign_by_id(self):
    c = campaign.Campaign()
    c = c.get_campaign_by_id(483494)
    c = json.loads(c)
    self.assertIn(c['msg_type'], 'success')

  def test_create_campaign(self):
    c = campaign.Campaign()

    data = {
      'advertiser_id': 162259,
      'ad_server_id': 9,
      'end_date': '2018-03-18T09:00:00',
      'goal_type': 'spend',
      'goal_value': '0.0001',
      'name': 'arun test campaign 03/06',
      'service_type': 'SELF',
      'start_date': '2018-03-16T23:59:00',
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

  def test_update_campaign(self):
    # initialize campaign instance
    c = campaign.Campaign()
    # get campaign by id
    # old_campaign = c.get_campaign_by_id(485277)
    # # # convert json str to json dict
    # old_campaign = json.loads(old_campaign)
    # del old_campaign['data']['id']
    # del old_campaign['data']['initial_start_date']
    # del old_campaign['data']['created_on']
    # del old_campaign['data']['updated_on']
    # del old_campaign['data']['entity_type']
    # del old_campaign['data']['goal_value']
    # del old_campaign['data']['use_mm_freq']
    # del old_campaign['data']['dcs_data_is_campaign_level']
    # del old_campaign['data']['frequency_optimization']
    # del old_campaign['data']['has_custom_attribution']
    # del old_campaign['data']['impression_cap_automatic']
    # del old_campaign['data']['minimize_multi_ads']
    # del old_campaign['data']['override_suspicious_traffic_filter']
    # del old_campaign['data']['restrict_targeting_to_deterministic_id']
    # del old_campaign['data']['restrict_targeting_to_same_device_id']
    # del old_campaign['data']['spend_cap_automatic']
    # del old_campaign['data']['total_budget']
    # del old_campaign['data']['status']
    # del old_campaign['data']['use_default_ad_server']
    # print 'OLD CAMPAIGN: ', old_campaign['data']



    # get campaign id to pass into save()
    # campaign_id = old_campaign['data']['id']
    data = {
      'advertiser_id': 162259,
      'ad_server_id': 9,
      # # 'end_date': '2018-03-12T09:00:00',
      # 'goal_type': 'spend',
      # 'goal_value': '0.0001',
      'name': 'test campaign on 03/07/2018',
      # 'service_type': 'SELF',
      # # 'start_date': '2018-03-11T23:59:00',
      # 'total_budget': 2,
    }

    updated_campaign = c.update_campaign(data, 485277)

    # self.assertIn(json.loads(updated_campaign)['data']['name'], 'this is arun suresh\'s test campaign on 03/06/2018')

  def test_get_budget_flights(self):
    c = campaign.Campaign()
    assert len(json.loads(c.get_budget_flights(485277))['data']) >= 1
