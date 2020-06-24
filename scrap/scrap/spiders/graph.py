import json

class Graph:
	def __init__(self):
		# the codes for actors and films are unique numbers, so we can simply each entry a list of numbers
		# the first number of an actor node could be their number and all the subsequent ones could be one for their films		
		self.actors = {}
		self.films = {}

	# actor and film nodes should store more than just their names
	# we could add star sign, height, and age 
	# each key could store an actor or film object 
	def new_actor(self, code, name):
		self.actors[code] = {"name": name, "films": []}

	def new_film(self, code, title):
		self.films[code] = {"title": title, "actors": []}

	def add_actor_data(self, code, yob, height, starsign):
		self.actors[code]['age'] = 2020 - yob
		self.actors[code]['height'] = height
		self.actors[code]['star sign'] = starsign 

	def add_film_data():
		pass

	# here we need to find the right entry and append the code to its list
	def add_actor_to_film(self, film, actor):
		# the dictionary stores keys as codes and values as lists of other codes
		self.films[film]["actors"].append(actor)

	def add_film_to_actor(self, actor, film):
		self.actors[actor]["films"].append(film)

	def contains_code(self, code, actor):
		if actor: 
			if code in self.actors:
				return True
			else: 
				return False
		else: 
			if code in self.films:
				return True
			else:
				return False

	# linear search, very inefficient but what are you gonna do? 
	def contains_name(self, name, actor):
		if actor:
			for actor in self.actors:
				if self.actors[actor]["name"] == name:
					return actor
			raise Exception("Graph does not contain %s" % name)
		else:
			for film in self.films:
				if self.films[film]["title"] == name:
					return film
			raise Exception("Graph does not contain %s" % name)

	# do we use these assuming the actor or film already exists, or should we double check that they do?
	# I feel like we can assume that they exist given the context in which we use them 	
	def actor_contains(self, actor, film):
		if film in self.actors[actor]["films"]: 
			return True 
		return False

	def film_contains(self, film, actor):
		if actor in self.films[film]["actors"]: 
			return True 
		return False

	def write_graph_to_file(self, a_file, f_file):
		f = open(a_file, "w")
		actor_json = json.dumps(self.actors, indent=4)
		f.write(actor_json)
		f.close()

		f = open(f_file, "w")
		film_json = json.dumps(self.films, indent=4)
		f.write(film_json)
		f.close()

	@staticmethod 
	def load_graph(a_file, f_file):
		graph = Graph()

		with open(a_file) as file:
			actors = json.load(file)

		with open(f_file) as file:
			films = json.load(file)

		graph.actors = actors
		graph.films = films
		return graph

# if we kept actors and films in order that could make accessing easier
# or perhaps we could use a hash map of some sort (dictionary)
# we could have actor objects which contain their code plus the indices of their films(?)
# we want to be able to stop at either films or actors, so both should start off with empty lists