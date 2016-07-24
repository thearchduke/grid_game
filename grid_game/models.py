'''
Models for GridGame
copyright Tynan Burke
www.tynanburke.com
all rights reserved
'''


class BaseGGObject(object):
	_gg_version = 'GridGame v0.1'

	def __init__(self, *args, **kwargs):
		super(BaseGGObject, self).__init__()

class Game(BaseGGObject):
	grid_type = 'hexagonal'
	tiles = []

class Tile(BaseGGObject):
	pass

game = None

def register_game():
	game = Game()