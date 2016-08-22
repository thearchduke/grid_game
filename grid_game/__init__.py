from models import *
from utils import *

from flask import Flask, render_template

app = Flask(__name__)
app.config['game_settings'] = GAME_SETTINGS
app.config['DEBUG'] = GAME_SETTINGS.debug

import grid_game.routes