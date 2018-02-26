from unittest import TestCase
from mediamathclient.mediamathclient import campaign
import os
import json

class TestMediaMathCampaign(TestCase):

  def test_connection(self):
    session_id = campaign.Campaign().get_connection().session_id
    self.assertIsNotNone(session_id)