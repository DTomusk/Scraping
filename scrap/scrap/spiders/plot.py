import networkx as nx 
import matplotlib.pyplot as plt
import plotly.graph_objects as go 

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

	edge_x = []
	edge_y = []

	fig = go.Figure()

	for edge in G.edges():
		print(edge)
		print(pos[edge[0]])
		print(pos[edge[0]][0])
		print(pos[edge[1]])
		edge_x.append(pos[edge[0]][0])
		edge_x.append(pos[edge[0]][1])
		edge_x.append(None)
		edge_y.append(pos[edge[1]][0])
		edge_y.append(pos[edge[1]][1])
		edge_y.append(None)

	edge_trace = go.Scatter(x=edge_x, y=edge_y, line=dict(width=0.5, color='#888'), hoverinfo='none', mode='lines')

	node_x = []
	node_y = []

	for node in G.nodes():
		x, y = pos[node]
		node_x.append(x)
		node_y.append(y)

	node_trace = go.Scatter(x=node_x, y=node_y, mode='markers', marker=dict(size=10))
	
	#print(edge_trace)

	fig = go.Figure(data=[edge_trace, node_trace], layout=go.Layout(title=go.layout.Title(text="Actors and films and such")))

	fig.show()

	#nx.draw_networkx(G, with_labels=False)
	#plt.show()