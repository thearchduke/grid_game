'''
Models for GridGame
copyright Tynan Burke
www.tynanburke.com
some rights reserved, GPL etc.
'''

from grid_game.models.base import BaseGGObject

class Game(BaseGGObject):
	'''
	Game object for GridGame
	holds tiles
	note that everything here is for square tiles right now
	'''
	gps_step = 1
	centroid = None

	@property
	def corners(self):
		tiles = sorted(self.tiles, key=lambda t: (t.lon, t.lat))
		tiles = [(t.lon, t.lat) for t in tiles]
		SW, NE = tiles[0], tiles[-1]
		return {
			'SW': (SW[0], SW[1]), 
			'NW': (SW[0], NE[1]),
			'NE': (NE[0], NE[1]),
			'SE': (NE[0], SW[1])
			}
	
	def is_in_game(self, test_lon, test_lat):
		corners = self.corners
		if test_lon < corners['SW'][0]:
			return False
		if test_lon > corners['SE'][0]:
			return False
		if test_lat < corners['SW'][1]:
			return False
		if test_lat > corners['NW'][1]:
			return False		
		return True

	def get_tile(self, x, y):
		out_tile = [t for t in self.tiles if t.x == x and t.y == y]
		if out_tile:
			return out_tile[0]
		else:
			return None

	def __init__(self, lon, lat, step):
		self.tiles = set()
		self.gps_step = step
		super(Game, self).__init__()


class Tile(BaseGGObject):
	game = None
	name = ''
	x,y = -1,-1
	'''x,y coordinates on the grid'''

	_allowed_resources = ['oil', 'water', 'labor', 'cash']

	lon,lat = 0,0
	'''lon,lat of SW corner'''
	#reminder: latitude describe north/south

	def neighbors(self):
		'''
		Get neighbors surrounding tile
		'''
		if not self.game:
			return 'tile not registered to a game'

		N = self.game.get_tile(self.x, self.y+1)
		NE = self.game.get_tile(self.x+1, self.y+1)
		E = self.game.get_tile(self.x+1, self.y)
		SE = self.game.get_tile(self.x+1, self.y-1)
		S = self.game.get_tile(self.x, self.y-1)
		SW = self.game.get_tile(self.x-1, self.y-1)
		W = self.game.get_tile(self.x-1, self.y)
		NW = self.game.get_tile(self.x-1, self.y+1)

		return {'N': N, 'NE': NE, 'E': E, 'SE': SE, 'S': S, 'SW': SW, 'W': W, 'NW': NW}

	def _bounding_box(self):
		'''
		gps bounding box of tile
		'''
		step = self.game.gps_step
		return {'NW': (self.lon, self.lat+step), 
			'NE': (self.lon+step, self.lat+step), 
			'SE': (self.lon+step, self.lat), 
			'SW': (self.lon, self.lat)}

	@property
	def coords(self):
		return (self.x, self.y)

	@classmethod
	def get_by_coords(cls, x, y):
		'''
		return tile x,y or None
		'''
		test = [t for t in cls.game.tiles if t.x == x and t.y == y]
		if test:
			return test[0]
		else:
			return None

	@classmethod
	def get_by_gps(cls, current_lon, current_lat):
		'''
		return tile containing current_lon and current_lat
		or None
		'''
		if not cls.game.is_in_game(current_lon, current_lat):
			return None
		sorted_lon = sorted(cls.game.tiles, key=lambda t: t.lon)
		x_index = None
		while not x_index:
			test = sorted_lon.pop()
			if test.lon <= current_lon:
				x_index = test
		sorted_lat = sorted(cls.game.tiles, key=lambda t: t.lat)
		filtered_sorted_lat = filter(lambda t: t.lon == x_index.lon, sorted_lat)
		result_tile = None
		while not result_tile:
			test = filtered_sorted_lat.pop()
			if test.lat <= current_lat:
				result_tile = test
		return result_tile

	@classmethod
	def register(cls, tiles, game):
		'''
		add tile or list/set of tiles to game
		'''
		if type(tiles) == Tile:
			cls.game = game
			game.tiles.add(tiles)
		elif type(tiles) == list or type(tiles) == set:
			tiles = set([t for t in tiles if type(t) == Tile])
			cls.game = game
			game.tiles.update(tiles)
		else:
			raise TypeError('register takes Tile objects or lists/sets of Tile objects')

	def __repr__(self):
		return '"%s": %s' % (self.name, self.coords)

	def __init__(self, x=None, y=None, lon=None, lat=None, name=None, game=None):
		self.x = x or None
		self.y = y or None
		self.lon = lon or 0
		self.lat = lat or 0
		self.name = name or 'default tile name'
		self.resources = {r:0 for r in self._allowed_resources}
		if game:
			Tile.register(self, game)
			self.game = game
		super(Tile, self).__init__()