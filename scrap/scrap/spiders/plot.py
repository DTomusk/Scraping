import networkx as nx 
import matplotlib.pyplot as plt

def plot_graph(data):
	G = nx.Graph()
	for actor in data.actors:
		for film in data.actors[actor][1]:
			G.add_node(data.films[film][0])
			G.add_edge(data.actors[actor][0], data.films[film][0])

	for film in data.films:
		for actor in data.films[film][1]:
			G.add_edge(data.films[film][0], data.actors[actor][0])
	nx.draw_networkx(G, with_labels=False)
	print("Graph nodes: ")
	print(G.nodes())
	print("Graph edges: ")
	print(G.edges())
	plt.savefig("my_plot.png")
	plt.show()