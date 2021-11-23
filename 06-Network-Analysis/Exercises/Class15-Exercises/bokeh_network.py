import networkx

from bokeh.io import output_notebook, show, save
from bokeh.models import Range1d, Circle, ColumnDataSource, MultiLine, EdgesAndLinkedNodes, NodesAndLinkedEdges, LabelSet
from bokeh.plotting import figure
from bokeh.plotting import from_networkx
from bokeh.palettes import Blues8, Reds8, Purples8, Oranges8, Viridis8, Spectral8
from bokeh.transform import linear_cmap
from networkx.algorithms import community

def make_interactive_network(G, labels=False, title='My Network', color_palette=Blues8, node_size='degree', node_color='modularity_class'):
    
    from networkx.algorithms import community

    # Get network info
    degrees = dict(networkx.degree(G))
    networkx.set_node_attributes(G, name='degree', values=degrees)
    betweenness_centrality = networkx.betweenness_centrality(G)
    networkx.set_node_attributes(G, name='betweenness', values=betweenness_centrality)
    communities = community.greedy_modularity_communities(G)
    
    # Create empty dictionaries
    modularity_color = {}
    modularity_class = {}
    #Loop through each community in the network
    for community_number, community in enumerate(communities):
        #For each member of the community, add their community number and a distinct color
        for name in community: 
            modularity_color[name] = Spectral8[community_number]
            modularity_class[name] = community_number

    networkx.set_node_attributes(G, modularity_color, 'modularity_color')
    networkx.set_node_attributes(G, modularity_class, 'modularity_class')

    #Choose colors for node and edge highlighting
    node_highlight_color = node_color
    edge_highlight_color = 'black'

    #Choose attributes from G network to size and color by — setting manual size (e.g. 10) or color (e.g. 'skyblue') also allowed


    #Pick a color palette — Blues8, Reds8, Purples8, Oranges8, Viridis8
    #color_palette = Blues8
    
    

    #Choose a title!
    title = title

    #Establish which categories will appear when hovering over each node
    HOVER_TOOLTIPS = [
           ("Character", "@index"),
            ("Degree", "@degree"),
             ("Modularity Class", "@modularity_class"),
            ("Modularity Color", "$color[swatch]:modularity_color"),
    ]

    #Create a plot — set dimensions, toolbar, and title
    plot = figure(tooltips = HOVER_TOOLTIPS,
                  tools="pan,wheel_zoom,save,reset", active_scroll='wheel_zoom',
                x_range=Range1d(-10.1, 10.1), y_range=Range1d(-10.1, 10.1), title=title)

    #Create a network graph object
    # https://networkx.github.io/documentation/networkx-1.9/reference/generated/networkx.drawing.layout.spring_layout.html
    network_graph = from_networkx(G, networkx.spring_layout, scale=10, center=(0, 0))

    #Set node sizes and colors according to node degree (color as category from attribute)
    if node_color == 'degree':
        #Set node sizes and colors according to node degree (color as spectrum of color palette)
        minimum_value_color = min(network_graph.node_renderer.data_source.data[node_color])
        maximum_value_color = max(network_graph.node_renderer.data_source.data[node_color])
        network_graph.node_renderer.glyph = Circle(size=node_size, fill_color=linear_cmap(node_color, color_palette, minimum_value_color, maximum_value_color))
    elif node_color == 'modularity_color':
        #node_color='modularity_color'
        network_graph.node_renderer.glyph = Circle(size=node_size, fill_color=node_color)
        #Set node highlight colors
        network_graph.node_renderer.hover_glyph = Circle(size=node_size, fill_color=node_highlight_color, line_width=2)
        network_graph.node_renderer.selection_glyph = Circle(size=node_size, fill_color=node_highlight_color, line_width=2)

    #Set edge opacity and width
    network_graph.edge_renderer.glyph = MultiLine(line_alpha=0.3, line_width=1)
    #Set edge highlight colors
    network_graph.edge_renderer.selection_glyph = MultiLine(line_color=edge_highlight_color, line_width=2)
    network_graph.edge_renderer.hover_glyph = MultiLine(line_color=edge_highlight_color, line_width=2)

        #Highlight nodes and edges
    network_graph.selection_policy = NodesAndLinkedEdges()
    network_graph.inspection_policy = NodesAndLinkedEdges()

    plot.renderers.append(network_graph)

    if labels == True:
        #Add Labels
        x, y = zip(*network_graph.layout_provider.graph_layout.values())
        node_labels = list(G.nodes())
        source = ColumnDataSource({'x': x, 'y': y, 'name': [node_labels[i] for i in range(len(x))]})
        labels = LabelSet(x='x', y='y', text='name', source=source, background_fill_color='white', text_font_size='10px', background_fill_alpha=.7)
        plot.renderers.append(labels)
    
    show(plot)
#save(plot, filename=f"{title}.html")