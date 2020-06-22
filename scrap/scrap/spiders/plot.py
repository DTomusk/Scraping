import networkx as nx 
import matplotlib.pyplot as plt

def plot_graph(data):
	G = nx.Graph()
	actor_nodes = []
	film_nodes = []
	for actor in data.actors:
		actor_nodes.append(data.actors[actor][0])
		G.add_node(data.actors[actor][0])
		for film in data.actors[actor][1]:
			G.add_node(data.films[film][0])
			G.add_edge(data.actors[actor][0], data.films[film][0])

	for film in data.films:
		film_nodes.append(data.films[film][0])
		for actor in data.films[film][1]:
			G.add_edge(data.films[film][0], data.actors[actor][0])

	pos = nx.spring_layout(G)

	nx.draw_networkx_nodes(G, pos, nodelist=actor_nodes, node_color='r', node_size=200, linewidths=0.5, node_shape='8', edgecolors='k')
	nx.draw_networkx_nodes(G, pos, nodelist=film_nodes, node_color='b', node_size=50, linewidths=0.1, edgecolors='k')
	nx.draw_networkx_edges(G, pos)

	#nx.draw_networkx(G, with_labels=False)
	print("Graph nodes: ")
	print(G.nodes())
	print("Graph edges: ")
	print(G.edges())
	plt.savefig("my_plot.png")
	plt.show()