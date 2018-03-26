from unittest import TestCase
from mediamathclient.mediamathclient import supply_source
import os
import json

class TestMediaMathSupplySource(TestCase):

  def test_connection(self):
    s = supply_source.get_connection()
    session_id = s.session_id
    self.assertIsNotNone(session_id)

  def test_get_supply_sources(self):
    s = supply_source.SupplySource()
    supply_sources = s.get_supply_sources()
    supply_sources = json.loads(supply_sources)
    self.assertIn(supply_sources['msg_type'], 'success')