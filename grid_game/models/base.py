class GAME_OPTS(object):
	def __init__(self):
		self.populate_tile_methods = ['fixed', 'random']
		self.populate_tile_method = 'random'
		self.allowed_resources = ['r1', 'r2', 'r3', 'r4']
		self.resource_costs = ['c1', 'c2', 'c3', 'c4']
		self.testing = True
		self.debug = True

class BaseGGObject(object):
	_gg_version = 'GridGame v0.1'
	_grid_type = 'square'
