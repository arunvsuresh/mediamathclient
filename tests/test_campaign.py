from unittest import TestCase
from mediamathclient.mediamathclient import campaign
import os
import json

class TestMediaMathCampaign(TestCase):

  def test_connection(self):
    session_id = campaign.Campaign().get_connection()
    self.assertIsNotNone(session_id)

  def test_get_campaigns(self):
    campaigns = campaign.Campaign().get_campaigns()
    self.assertTrue('"msg_type": "success"', campaigns)
