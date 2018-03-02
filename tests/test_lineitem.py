from unittest import TestCase
from mediamathclient.mediamathclient import lineitem
import os
import json

class TestMediaMathLineItem(TestCase):

  def test_connection(self):
    line_item = lineitem.get_connection()
    session_id = line_item.session_id
    self.assertIsNotNone(session_id)

  def test_get_lineitem_by_id(self):
    line_item = lineitem.LineItem()
    line_item = line_item.get_lineitem_by_id(1188752)
    line_item = json.loads(line_item)
    self.assertIn(line_item['msg_type'], 'success')

  def test_get_lineitems_by_campaign(self):
    line_item = lineitem.LineItem()
    line_item = line_item.get_lineitems_by_campaign(243821)
    line_item = json.loads(line_item)
    self.assertIn(line_item['msg_type'], 'success')

  def test_create_lineitem(self):
    line_item = lineitem.LineItem()

    data = {
      'campaign_id': 243821,
      'name': 'arun test line item 03/02/2018',
      'start_date': '2018-03-02T23:59:00+0000',
      'end_date': '2018-03-10T09:00:00+0000',
      'budget': 2,
      'pacing_amount': 0.01,
      'goal_type': 'spend',
      'use_optimization': 0,
      'type': 'GBO',
    }
    new_lineitem = line_item.create_lineitem(data)
    new_lineitem = json.loads(new_lineitem)
    self.assertIn(new_lineitem['msg_type'], 'success')

  # test when missing required field (campaign_id in this case)
  def test_error_in_create_lineitem(self):
    line_item = lineitem.LineItem()

    data = {
      'name': 'arun test line item',
      'start_date': '2018-03-02T23:59:00+0000',
      'end_date': '2018-03-10T09:00:00+0000',
      'budget': 2,
      'pacing_amount': 0.01,
      'goal_type': 'spend',
      'use_optimization': 0,
      'type': 'GBO',
    }
    new_lineitem = line_item.create_lineitem(data)
    new_lineitem = json.loads(new_lineitem)
    self.assertIn(new_lineitem['msg_type'], 'error')
