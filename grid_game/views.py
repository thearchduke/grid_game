from models import *
from utils import *

from flask import Flask, render_template

app = Flask(__name__)

@app.route('/sandbox')
def index():
	width = 10
	height = 7
	game = Game(lon=-122.425039, lat=37.77495, gps_step=0.0008, start_width=width, start_height=height)
	start = game.get_tile_by_coords(1,1)
	end = game.get_tile_by_coords(width+1,height+1)
	sample_path = shortest_resource_path(game, start, end, 'c1')
	path_to_render = [game.get_tile_by_coords(node[0], node[1]) for node in sample_path['path']]
	app.config['game_settings'] = GAME_SETTINGS

	return render_template('map.html', game=game, path=path_to_render)

	#with open('map.html', 'wb') as f:
		#f.write(template.render(settings=GAME_SETTINGS, game=game).encode('UTF-8'))
