'''
Models for GridGame
copyright Tynan Burke
www.tynanburke.com
some rights reserved, GPL etc.
'''
import random

from base import BaseGGObject, GAME_SETTINGS
from resources import BaseResource, BaseResourceStore
import networkx as nx


class Game(BaseGGObject):
	'''
	Game object for GridGame
	holds tiles
	note that everything here is for square tiles right now
	'''

	@property
	def corners(self):
		'''
		returns extreme corners of the game grid
		'''
		tiles = sorted(self.tiles, key=lambda t: (t.lon, t.lat))
		tiles = [(t.lon, t.lat) for t in tiles]
		SW, NE = tiles[0], tiles[-1]
		return {
			'SW': {'lon': SW[0], 'lat': SW[1]}, 
			'NW': {'lon': SW[0], 'lat': NE[1]},
			'NE': {'lon': NE[0], 'lat': NE[1]},
			'SE': {'lon': NE[0], 'last': SW[1]}
			}
	
	def is_in_game(self, test_lat, test_lon):
		'''
		returns True if tile within bounds of game @corners else false
		'''
		corners = self.corners
		if test_lon < corners['SW']['lon']:
			return False
		if test_lon > corners['SE']['lon']:
			return False
		if test_lat < corners['SW']['lat']:
			return False
		if test_lat > corners['NW']['lat']:
			return False		
		return True

	def get_tile_by_coords(self, x, y):
		'''
		get tile by coordinates
		'''
		out_tile = [t for t in self.tiles if t.x == x and t.y == y]
		if out_tile:
			return out_tile[0]
		else:
			return None

	def get_tile_by_gps(self, current_lat, current_lon):
		'''
		return tile containing current_lon and current_lat
		or None
		'''
		if not self.is_in_game(current_lat, current_lon):
			return None
		sorted_lon = sorted(self.tiles, key=lambda t: t.lon)
		x_index = None
		while not x_index:
			test = sorted_lon.pop()
			if test.lon <= current_lon:
				x_index = test
		sorted_lat = sorted(self.tiles, key=lambda t: t.lat)
		filtered_sorted_lat = filter(lambda t: t.lon == x_index.lon, sorted_lat)
		result_tile = None
		while not result_tile:
			test = filtered_sorted_lat.pop()
			if test.lat <= current_lat:
				result_tile = test
		return result_tile

	def _populate(self, start_width, start_height):
		'''
		populates the game grid with blank tiles with default properties
		constructs game.graph with default edge resource costs for all edges including diagonals
		'''
		lon_limit = self.sw_lon + start_width * self.gps_step - self.gps_step*.1
		lat_limit = self.sw_lat + start_height * self.gps_step - self.gps_step*.1
		tiles = []
		x, y = 1, 1
		current_lat = self.sw_lat

		while current_lat < lat_limit:
			x = 1
			current_lon = self.sw_lon
			while current_lon < lon_limit:
				t = Tile(x=x, y=y, lon=current_lon, lat=current_lat,
					populate_tile_method=GAME_SETTINGS.populate_tile_method)
				current_lon += self.gps_step
				x += 1
				tiles.append(t)
			current_lat += self.gps_step
			y += 1
		self.add_tiles(tiles, populate=True)

	def add_tiles(self, tiles, populate=False):
		'''
		adds tile or tiles to game.tiles, game.graph
		returns False, skips game.graph operations if no difference from previous game state
		else returns True
		'''
		if type(tiles) != list:
			tiles = [tiles]
		cache = set([t for t in self.tiles])
		self.tiles.update(tiles)
		if self.tiles == cache:
			return False
		for t in tiles:
			t.game = self
			self.graph.add_node(t.coords)
			neighbors = t.neighbors()
			for n in neighbors:
				if neighbors[n]:
					if populate:
						self.graph.add_edge(t.coords, neighbors[n].coords, t.costs)
		return True

	def __init__(self, **kwargs):
		self.lon = kwargs.get('lon')
		self.lat = kwargs.get('lat')
		self.gps_step = kwargs.get('gps_step')
		self.sw_lon = self.lon - (self.gps_step * kwargs.get('start_width')/2.0)
		self.sw_lat = self.lat - (self.gps_step * kwargs.get('start_height')/2.0)

		if not (self.gps_step and self.sw_lat and self.sw_lon and 
			kwargs.get('start_width') and kwargs.get('start_height')):

			raise ValueError("a game needs a sw_lon, sw_lat, start_width, start_height, and gps_step")

		self.tiles = set()
		self.graph = nx.Graph()

		GAME_SETTINGS.populate_tile_method = kwargs.get('populate_tile_method') or GAME_SETTINGS.populate_tile_method
		if GAME_SETTINGS.populate_tile_method not in GAME_SETTINGS.populate_tile_methods:
			raise ValueError("populate_tile_method must be allowed in GAME_SETTINGS: %s" % GAME_SETTINGS.populate_tile_method)

		self._populate(kwargs.get('start_width'), kwargs.get('start_height'))

		super(Game, self).__init__()


class Tile(BaseGGObject):
	'''
	Tile object for GridGame
	'''
	def neighbors(self):
		'''
		Get neighbors surrounding tile
		includes diagonals 
		'''
		if not self.game:
			return 'tile not registered to a game'

		N = self.game.get_tile_by_coords(self.x, self.y+1)
		NE = self.game.get_tile_by_coords(self.x+1, self.y+1)
		E = self.game.get_tile_by_coords(self.x+1, self.y)
		SE = self.game.get_tile_by_coords(self.x+1, self.y-1)
		S = self.game.get_tile_by_coords(self.x, self.y-1)
		SW = self.game.get_tile_by_coords(self.x-1, self.y-1)
		W = self.game.get_tile_by_coords(self.x-1, self.y)
		NW = self.game.get_tile_by_coords(self.x-1, self.y+1)

		return {'N': N, 'NE': NE, 'E': E, 'SE': SE, 'S': S, 'SW': SW, 'W': W, 'NW': NW}

	@property
	def corners(self):
		'''
		gps bounding box of tile
		'''
		step = self.game.gps_step
		return {'NW': {'lon': self.lon, 'lat': self.lat+step}, 
			'NE': {'lon': self.lon+step, 'lat': self.lat+step}, 
			'SE': {'lon': self.lon+step, 'lat': self.lat}, 
			'SW': {'lon': self.lon, 'lat': self.lat}}

	@property
	def center(self):
		'''
		gps centroid
		Tile.lon, Tile.lat are SW corner
		'''
		step = self.game.gps_step
		return {'lon': self.lon + step/2, 'lat': self.lat + step/2}

	@property
	def coords(self):
		return (self.x, self.y)

	@classmethod
	def shortest_path(cls, start, end, resource=None):
		if not (start.game and end.game):
			raise KeyError('start and end must have associated games')
		elif start.game != end.game:
			raise ValueError('start and end must have the same game')
		if resource:
			pass
		else:
			pass

	def __repr__(self):
		return '"%s": %s' % (self.name, self.coords)

	def __init__(self, **kwargs):
		'''
		reminder: lon, lat are SW corner
		'''
		self.x = kwargs.get('x') or None
		self.y = kwargs.get('y') or None
		self.lon = kwargs.get('lon') or 0
		self.lat = kwargs.get('lat') or 0
		self.name = kwargs.get('name') or 'default tile name'

		pop_method = kwargs.get('populate_tile_method') or GAME_SETTINGS.populate_tile_method
		allowed_resources = kwargs.get('allowed_resources') or GAME_SETTINGS.allowed_resources
		resource_costs = kwargs.get('resource_costs') or GAME_SETTINGS.resource_costs

		if pop_method == 'random':
			self.costs = kwargs.get('costs') or {r:random.randint(1,100) for r in resource_costs}
			self.resources = kwargs.get('resources') or {r:random.randint(1,100) for r in allowed_resources}
		elif pop_method == 'fixed':
			self.costs = kwargs.get('costs') or {r:100 for r in resource_costs}
			self.resources = kwargs.get('resources') or {r:0 for r in allowed_resources}
		else:
			raise ValueError('unknown populate_tile_method: %s' % pop_method)

		if kwargs.get('game'):
			Tile.register(self, kwargs.get('game'))
			self.game = kwargs.get('game')
		else:
			self.game = None

		super(Tile, self).__init__()
