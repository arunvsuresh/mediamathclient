from base import Base

class Campaign(Base):

  obj_name = 'campaigns'

  # def __init__(self, data=None, omg_campaign=None):
  #   self.data = data
  #   self.omg_campaign = omg_campaign

  def get_campaigns_by_advertiser(self, advertiser_id):
    advertiser_id = int(advertiser_id)
    url = self.generate_url() + "/limit/advertiser={0}".format(advertiser_id)
    return self.call_mm_api('GET', url)

  def get_budget_flights(self, campaign_id):
    campaign_id = int(campaign_id)
    url = self.generate_url() + "/" + str(campaign_id) + "/budget_flights?full=*"
    return self.call_mm_api('GET', url)
