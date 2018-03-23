from unittest import TestCase
from mediamathclient.mediamathclient import creative
import os
import json

class TestMediaMathcreative(TestCase):

  def test_connection(self):
    c = creative.Creative()
    session_id = c.t1.session_id
    self.assertIsNotNone(session_id)

  def test_get_creative_by_id(self):
    c = creative.Creative()
    c = c.get_by_id(110640)
    c = json.loads(c)
    self.assertIn(c['msg_type'], 'success')

  def test_get_creatives_by_lineitem(self):
    c = creative.Creative()
    creatives = c.get_creatives_by_lineitem(1197492)
    c = json.loads(creatives)
    self.assertIn(c['msg_type'], 'success')

  # pass in bad data to test for proper error handling
  def test_error_in_get_creatives_by_lineitem(self):
    c = creative.Creative()
    creatives = c.get_creatives_by_lineitem('a')
    c = json.loads(creatives)
    self.assertIn(c['msg_type'], 'error')
