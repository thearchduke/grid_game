from grid_game.models.game import *
from grid_game.models.resources import *

game = Game(lon=1, lat=1, gps_step=0.5, start_width=6, start_height=10)
#print game.graph.edges(data=True)
print game.get_tile_by_gps(1.3,2.9)
#print game.get_tile(1,1)
#print game.graph.edges(data=True)
#t14 = Tile(x=1,y=4)
#t41 = Tile(x=4,y=1)
#game.add_tiles([t14, t41])
#print help(game.graph.node)
#print game.get_tile(1,4)