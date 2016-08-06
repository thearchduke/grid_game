from grid_game.models import *
from grid_game.utils import *


game = Game(lon=1, lat=1, gps_step=0.5, start_width=6, start_height=6)
start = game.get_tile_by_coords(1,1)
end = game.get_tile_by_coords(6,6)
print shortest_resource_path(game, start, end, 'c1')
'''
path = nx.shortest_path(game.graph, (1,1), (6,6), weight='r1')
print path

game = Game(lon=1, lat=1, gps_step=0.5, start_width=6, start_height=6)
path = nx.shortest_path_length(game.graph, (1,1), (6,6), weight='r1')
print path

game = Game(lon=1, lat=1, gps_step=0.5, start_width=6, start_height=6)
path = nx.shortest_path_length(game.graph, (1,1), (6,6), weight='r1')
print path
#print game.graph.edges(data=True)[0]
#for edge in game.graph.edges(data=True):
	#print edge


game2 = Game(lon=1, lat=1, gps_step=0.5, start_width=6, start_height=6, populate_tile_method = 'fixed')
path = nx.shortest_path_length(game2.graph, (1,1), (6,6), weight='r1')
print path
#print game2.graph.edges(data=True)[0]
#for edge in game2.graph.edges(data=True):
	#print edge

#print game.get_tile(1,1)
#print game.graph.edges(data=True)
#t14 = Tile(x=1,y=4)
#t41 = Tile(x=4,y=1)
#game.add_tiles([t14, t41])
#print help(game.graph.node)
#print game.get_tile(1,4)
'''