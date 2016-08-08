from base import BaseGGObject, GAME_SETTINGS

class BaseResource(BaseGGObject):
	'''
	A GridGame resource type, e.g. 'oil'
	'''

	def __init__(self, **kwargs):
		name = kwargs.get('name')

		super(BaseResource, self).__init__()
		pass


class BaseResourceStore(BaseGGObject):
	'''
	A GridGame resource store. Implements a player or tile 
	having a certain amount of a Resource.
	'''

	def harvest(self, amt):
		'''
		remove amt from self.amount
		NOTE: returns amount removed, not necessarily amount attempted
		'''
		if self.amount - amt < 0:
			out = self.amount
			self.amount = 0
			return out
		self.amount -= amt
		return amt

	def grow(self, amt):
		'''
		add amt to self.amount
		'''
		self.amount += amt
		if self.amount > self.maximum:
			self.amount = self.maximum


	def __init__(self, **kwargs):
		self.kind = 'base resource'
		self.amount = kwargs.get('amount') or GAME_SETTINGS.resource_start_amt
		self.maximium = kwargs.get('maximum') or GAME_SETTINGS.resource_max

		super(BaseResourceStore, self).__init__()

