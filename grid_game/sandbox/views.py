from grid_game import app
from grid_game.helpers import *
from grid_game.models import *
from grid_game.utils import *

from flask import render_template

try:
	import cPickle as pickle
except:
	import pickle
import random
import logging



def _load_sandbox_game():
	with open('game_foursquare.p', 'rb') as f:
		game = pickle.load(f)
	return game

def checkin_page():
	return render_template('checkin.html')

def do_checkin(lat, lon):
	game = _load_sandbox_game()
	lat, lon = float(lat), float(lon)
	tile = game.get_tile_by_gps(lat, lon)
	return render_template('map_checkin.html', game=game, tile=tile)

def index(resource_kind):
	game = _load_sandbox_game()
	start = game.get_tile_by_coords(1,1)
	end = game.get_tile_by_coords(10,1)
	sample_path = shortest_resource_path(game, start, end, resource_kind)
	path_to_render = [game.get_tile_by_coords(node[0], node[1]) for node in sample_path['path']]

	f = lambda a,b: a if (a > b) else b
	max_cost = reduce(f, [t.resources[resource_kind] for t in game.tiles])

	return render_template('map_foursquare.html', game=game, path=path_to_render, kind=resource_kind, max_cost=max_cost)

def random_gen():
	width = 22
	height = 26 
	game = Game(lon=-122.427039, lat=37.76795, gps_step=0.0008, start_width=width, start_height=height)
	start = game.get_tile_by_coords(1,1)
	end = game.get_tile_by_coords(width,height)
	sample_path = shortest_resource_path(game, start, end, 'c1')
	path_to_render = [game.get_tile_by_coords(node[0], node[1]) for node in sample_path['path']]

	fname = 'game_random_%s' % random.randint(1,1000)
	with open(fname, 'wb') as f: pickle.dump(game, f)
	return render_template('map.html', game=game, path=path_to_render)

def fixed_gen():
	width = 10
	height = 11 
	GAME_SETTINGS.populate_tile_method = 'fixed'
	game = Game(lon=-122.427039, lat=37.76795, gps_step=0.002, start_width=width, start_height=height)
	start = game.get_tile_by_coords(1,1)
	end = game.get_tile_by_coords(width,height)
	sample_path = shortest_resource_path(game, start, end, 'c1')
	path_to_render = [game.get_tile_by_coords(node[0], node[1]) for node in sample_path['path']]

	s,e = FoursquareHelper.venues_in_tile(start), FoursquareHelper.venues_in_tile(end)
	print s,e
	print len(s['venues']), len(e['venues'])

	fname = 'game_random_fixed.p'
	with open(fname, 'wb') as f: pickle.dump(game, f)
	return render_template('map.html', game=game, path=path_to_render)

def fixed_and_foursquare():
	with open('game_random_fixed.p', 'rb') as f:
		game = pickle.load(f)		
	n = 1
	for tile in game.tiles:
		print n, len(game.tiles)
		tile.resources = {
			'coffee': FoursquareHelper.venues_in_tile_by_cat(tile, 'coffee'),
			'transport': FoursquareHelper.venues_in_tile_by_cat(tile, 'transport'),
			'food': FoursquareHelper.venues_in_tile_by_cat(tile, 'food'),
			'entertainment': FoursquareHelper.venues_in_tile_by_cat(tile, 'entertainment'),
			'labor': FoursquareHelper.venues_in_tile_by_cat(tile, 'labor')
		}
		n += 1
	with open('game_foursquare.p', 'wb') as f:
		pickle.dump(game, f)

	return "<h1>hi</h1>"