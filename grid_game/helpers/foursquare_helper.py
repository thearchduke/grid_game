import foursquare

from grid_game.models import *


class FoursquareHelper(BaseGGObject):
	client = foursquare.Foursquare(client_id=GAME_SETTINGS.FOURSQUARE_CLIENT_ID, 
		client_secret=GAME_SETTINGS.FOURSQUARE_CLIENT_SECRET)

	@classmethod
	def venues_in_tile_by_cat(cls, tile, category, limit=50):
		category_map = {
			'coffee': '4bf58dd8d48988d1e0931735',
			'bar': '4bf58dd8d48988d116941735',
			'entertainment': '4d4b7104d754a06370d81259',
			'nightlife': '4d4b7105d754a06376d81259',
			'food': '4d4b7105d754a06374d81259',
			'residence': '4e67e38e036454776db1fb3a',
			'shopping': '4d4b7105d754a06378d81259',
			'transport': '4d4b7105d754a06379d81259',
			'knowledge': '4d4b7105d754a06372d81259',
			'outdoors': '4d4b7105d754a06377d81259',
			'labor': '4d4b7105d754a06375d81259',
		}

		results = cls.client.venues.search(params={
			'limit': limit,
			'intent': 'browse',
			'categoryId': category_map[category],
			'sw': "%f,%f" % (tile.corners['SW']['lat'], tile.corners['SW']['lon']),
			'ne': "%f,%f" % (tile.corners['NE']['lat'], tile.corners['NE']['lon']),
			})

		return results

	@classmethod
	def venues_in_tile(cls, tile, limit=50):
		results = cls.client.venues.search(params={
			'limit': limit,
			'intent': 'browse',
			'sw': "%f,%f" % (tile.corners['SW']['lat'], tile.corners['SW']['lon']),
			'ne': "%f,%f" % (tile.corners['NE']['lat'], tile.corners['NE']['lon']),
			})

		return results