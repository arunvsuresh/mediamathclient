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
    li = line_item.get_lineitem_by_id(1197492)
    li = json.loads(li)
    self.assertIn(li['msg_type'], 'success')

  def test_get_lineitems_by_campaign(self):
    line_item = lineitem.LineItem()
    li = line_item.get_lineitems_by_campaign(243821)
    li = json.loads(li)
    self.assertIn(li['msg_type'], 'success')

  def test_create_lineitem(self):
    line_item = lineitem.LineItem()

    data = {
      'campaign_id': 243821,
      'name': 'arun test line item 03/02/2018',
      'start_date': '2018-03-15T23:59:00+0000',
      'end_date': '2018-03-16T09:00:00+0000',
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


  def test_update_lineitem(self):
    # initialize line item instance
    line_item = lineitem.LineItem()

    # get line item by id
    # old_lineitem = line_item.get_lineitem_by_id(1188752)
    #
    # # convert json str to json dict
    # old_lineitem = json.loads(old_lineitem)
    # # get line item id to pass into save()
    # lineitem_id = old_lineitem['data']['id']

    data = {
      'campaign_id': 243821,
      'name': 'arun\'s test line item 03/06/2018',
      'budget': 2,
      'pacing_amount': 0.01,
      'goal_type': 'spend',
      'use_optimization': 0,
      'type': 'GBO',
    }

    updated_lineitem = line_item.update_lineitem(data, 1188752)
    self.assertIn(json.loads(updated_lineitem)['data']['name'], 'arun\'s test line item 03/06/2018')

  def test_assign_sitelist_to_strategy(self):
    line_item = lineitem.LineItem()
    li = line_item.assign_sitelist_to_strategy(1197492, [117705, 117706])
    li = json.loads(li)
    self.assertIn(li['msg_type'], 'success')

  def test_remove_sitelist_from_strategy(self):
    line_item = lineitem.LineItem()
    li = line_item.remove_sitelist_from_strategy(1197492, [117705, 117706])
    li = json.loads(li)
    self.assertIn(li['msg_type'], 'success')

  def test_update_strategy_domain_restrictions(self):
    line_item = lineitem.LineItem()
    li = line_item.update_strategy_domain_restrictions(1197492, ['youtube.com'])
    li = json.loads(li)
    self.assertIn(li['msg_type'], 'success')

  def test_set_deal_targeting_for_strategy(self):
    line_item = lineitem.LineItem()
    li = line_item.set_deal_targeting_for_strategy(1197492, [63505,79600])
    li = json.loads(li)
    self.assertIn(li['msg_type'], 'success')

  def test_set_strategy_exchanges(self):
    line_item = lineitem.LineItem()
    li = line_item.set_strategy_exchanges(1197492, [159])
    li = json.loads(li)
    self.assertIn(li['msg_type'], 'success')

  def test_get_deals(self):
    line_item = lineitem.LineItem()
    li = line_item.get_deals()
    li = json.loads(li)
    self.assertIn(li['msg_type'], 'success')

  # def test_get_deals_by_advertiser(self):
  #   line_item = lineitem.LineItem()
  #   li = line_item.get_deals_by_advertiser(100429)
  #   print li
    # li = json.loads(li)['data']
    # print len(li)
    # self.assertIn(li['msg_type'], 'success')

