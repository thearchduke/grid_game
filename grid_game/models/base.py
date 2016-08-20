import ConfigParser
import datetime

class GAME_OPTS(object):
	def __init__(self):
		self.populate_tile_methods = ['fixed', 'random']
		self.populate_tile_method = 'random'
		self.allowed_resources = ['r1', 'r2', 'r3', 'r4']
		self.resource_costs = ['c1', 'c2', 'c3', 'c4']
		self.resource_start_amt = 100
		self.resource_max = 500		
		self.testing = True
		self.debug = True

		# secure stuff
		Config = ConfigParser.ConfigParser()
		Config.read('grid_game/config.ini')
		self.GOOGLE_MAPS_API_KEY = Config.get("Google", "MAPS_API_KEY")


class BaseGGObject(object):
	_gg_version = 'GridGame v0.1'
	_grid_type = 'square'

	def __init__(self):
		self.created = datetime.datetime.now()
		super(BaseGGObject, self).__init__()

GAME_SETTINGS = GAME_OPTS()