from grid_game import app
from models import *
from utils import *

import sandbox

app.add_url_rule('/sandbox/index', 'sandbox.index', sandbox.views.index)
app.add_url_rule('/sandbox/fixed_gen', 'sandbox.fixed_gen', sandbox.views.fixed_gen)
app.add_url_rule('/sandbox/<string:resource_kind>/view', 'sandbox.index', sandbox.views.index)
app.add_url_rule('/sandbox/checkin', 'sandbox.checkin', sandbox.views.checkin_page)
app.add_url_rule('/sandbox/checkin/<lat>&<lon>', 'sandbox.checkin.lat_lon', sandbox.views.do_checkin)