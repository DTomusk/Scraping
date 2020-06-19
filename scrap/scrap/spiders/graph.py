import json

class Graph:
	def __init__(self):
		# the codes for actors and films are unique numbers, so we can simply each entry a list of numbers
		# the first number of an actor node could be their number and all the subsequent ones could be one for their films		
		self.actors = {}
		self.films = {}

	def new_actor(self, code):
		self.actors[code] = []

	def new_film(self, code):
		self.films[code] = []

	# here we need to find the right entry and append the code to its list
	def add_actor_to_film(self, film, actor):
		# the dictionary stores keys as codes and values as lists of other codes
		self.films[film].append(actor)

	def add_film_to_actor(self, actor, film):
		self.actors[actor].append(film)

	def write_graph_to_file(self, filename):
		f = open(filename, "w")
		actor_json = json.dumps(self.actors)
		film_json = json.dumps(self.films)

		f.write("Actors: ")
		f.write(actor_json+"\n")
		f.write("Films: ")
		f.write(film_json)

		f.close()


# if we kept actors and films in order that could make accessing easier
# or perhaps we could use a hash map of some sort (dictionary)
# we could have actor objects which contain their code plus the indices of their films(?)
# we want to be able to stop at either films or actors, so both should start off with empty lists