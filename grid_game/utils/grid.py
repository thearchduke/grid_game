from grid_game.models import Game, Tile
import networkx as nx


##TODO: These should be instance methods on Game
#		Or tile
#		Or both! (both)
##TODO: associated weights (costs)/resources abstraction in Resource models

def shortest_resource_path(game, start, end, cost):
	path = nx.shortest_path(game.graph, start.coords, end.coords, weight=cost)
	length = resource_path_length(game, path, cost)
	return {'path': path, 'length': length}

def resource_path_length(game, path, cost):
	length = 0
	for node in path:
		tile = game.get_tile_by_coords(node[0], node[1])
		l = tile.costs[cost]
		length += l
	return length