import networkx as nx 
import plotly.graph_objects as go 

def plot_graph(data):
	G = nx.Graph()
	
	# needs to be a condition for adding film nodes, such as rating or popularity 
	for actor in data.actors:
		G.add_node(data.actors[actor]["name"], types='actor')
		for film in data.actors[actor]["films"]:
			G.add_node(data.films[film]["title"], types='film')
			G.add_edge(data.actors[actor]["name"], data.films[film]["title"])

	pos = nx.spring_layout(G)

	edge_x = []
	edge_y = []

	fig = go.Figure()
 
	for edge in G.edges():
		x1, y1 = pos[edge[0]]
		x2, y2 = pos[edge[1]]
		edge_x.append(x1)
		edge_x.append(x2)
		edge_y.append(y1)
		edge_y.append(y2)

	edge_trace = go.Scatter(x=edge_x, y=edge_y, line=dict(width=0.5, color='#888'), hoverinfo='none', mode='lines')

	node_x = []
	node_y = []
	names = []
	colors = []

	for node in G.nodes():
		x, y = pos[node]
		node_x.append(x)
		node_y.append(y)
		names.append(node)
		# check color attribute of node to assign the right colour 
		if G.node[node]['types'] == 'actor':
			colors.append("rgb(0, 0, 240)")
		else:
			colors.append("rgb(240, 0, 0)")

	# set hover info to be name or title 
	node_trace = go.Scatter(x=node_x, y=node_y, mode='markers', marker=dict(size=10, color=colors), hovertext=names)

	fig = go.Figure(data=[edge_trace, node_trace], layout=go.Layout(title=go.layout.Title(text="Actors and films and such")))

	fig.show()