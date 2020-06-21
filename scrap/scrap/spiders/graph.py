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

	def graph_contains(self, code, actor):
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

	# do we use these assuming the actor or film already exists, or should we double check that they do?
	# I feel like we can assume that they exist given the context in which we use them 	
	def actor_contains(self, actor, film):
		if film in self.actors[actor]:
			return True
		else:
			return False 

	def film_contains(self, film, actor):
		if actor in self.films[film]:
			return True
		else:
			return False 

	def write_graph_to_file(self, filename):
		f = open(filename, "w")
		actor_json = json.dumps(self.actors, indent=4)
		film_json = json.dumps(self.films, indent=4)

		f.write("Actors: ")
		f.write(actor_json+"\n")
		f.write("Films: ")
		f.write(film_json)

		f.close()


# if we kept actors and films in order that could make accessing easier
# or perhaps we could use a hash map of some sort (dictionary)
# we could have actor objects which contain their code plus the indices of their films(?)
# we want to be able to stop at either films or actors, so both should start off with empty lists