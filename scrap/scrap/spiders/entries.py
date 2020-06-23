class Actor():
	def __init__(self, name):
		self.name = name
		self.films = []

	def get_name(self):
		return name 

	def add_data(age, height, starsign):
		self.age = age
		self.height = height
		self.starsign = starsign

	def add_film(self, film_code):
		self.films.append(film_code)

	def contains(self, film_code):
		if film_code in self.films:
			return True
		else:
			return False

class Film():
	def __init__(self, title):
		self.title = title
		self.actors = []

	def add_data(year, rating, gross):
		self.year = year
		self.rating = rating
		self.gross = gross

	def add_actor(self, actor_code):
		self.actors.append(actor_code)

	def contains(self, actor_code):
		if actor_code in self.actors:
			return True
		else:
			return False

# actors is a dictionary of dictionaries, each actor has keys name, age, starsign whatever 