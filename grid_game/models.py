'''
Models for GridGame
copyright Tynan Burke
www.tynanburke.com
all rights reserved
'''


class BaseGGObject(object):
	_gg_version = 'GridGame v0.1'

	'''
	def __init__(self, *args, **kwargs):
		super(BaseGGObject, self).__init__()
	'''

class Game(BaseGGObject):
	'''
	note that everything here is for square tiles right now
	'''
	tiles = set()
	gps_step = 1

	def get_tile(self, x, y):
		test = [t for t in self.tiles if t.x == x and t.y == y]
		if test:
			return test[0]
		else:
			return None


class Tile(BaseGGObject):
	game = None
	name = ''
	x,y = -1,-1
	'''x,y coordinates on the grid'''

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

	def bounding_box(self):
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
	def point_in_tile(cls, current_lon, current_lat)
		sorted_tiles_lon = sorted(cls.game.tiles, key=lambda t: t.lon)
		x_index = None
		while not x_index:
			test = sorted_tiles_lon.pop()
			if test.lon <= current_lon:
				x_index = test
		if not x_index:
			return None


		sorted_tiles_lat = sorted(cls.game.tiles, key=lambda t: t.lat)


	@classmethod
	def register(cls, tiles, game):
		'''
		add tile or list/set of tiles to game
		'''
		if type(tiles) == Tile:
			game.tiles.add(tiles)
		elif type(tiles) == list or type(tiles) == set:
			tiles = set([t for t in tiles if type(t) == Tile])
			cls.game = game
			game.tiles.update(tiles)
		else:
			raise TypeError('register takes Tile objects or lists/sets of Tile objects')


	def __repr__(self):
		return '"%s": %s' % (self.name, self.coords)

	def __init__(self, x=None, y=None, name=None):
		self.x = x or -1
		self.y = y or -1
		self.name = name or 'default tile name'
		super(Tile, self).__init__()