import plotly.graph_objects as go
import networkx as nx
from plotly.subplots import make_subplots

# Create a figure with 2 rows, 1 column
fig = make_subplots(rows=2, cols=1, 
                    subplot_titles=("Graph Formation", "Graph Convolutional Network (GCN)"),
                    vertical_spacing=0.2,
                    specs=[[{"type": "xy"}], [{"type": "xy"}]])

# ===== GRAPH FORMATION (TOP) =====
# Create a star graph
G_formation = nx.star_graph(8)
pos_formation = nx.spring_layout(G_formation, seed=42)

# Create node coordinates
node_x_formation = []
node_y_formation = []
for node in G_formation.nodes():
    x, y = pos_formation[node]
    node_x_formation.append(x)
    node_y_formation.append(y)

# Create node trace for formation
node_trace_formation = go.Scatter(
    x=node_x_formation,
    y=node_y_formation,
    mode='markers',
    marker=dict(
        size=20,
        color=['pink' if node == 0 else 'lightblue' for node in G_formation.nodes()],
        line=dict(width=2, color='black')
    ),
    text=[f"Node {i}" for i in G_formation.nodes()],
    hoverinfo='text'
)

# Create edge trace for formation
edge_x_formation = []
edge_y_formation = []
for edge in G_formation.edges():
    x0, y0 = pos_formation[edge[0]]
    x1, y1 = pos_formation[edge[1]]
    edge_x_formation.extend([x0, x1, None])
    edge_y_formation.extend([y0, y1, None])

edge_trace_formation = go.Scatter(
    x=edge_x_formation,
    y=edge_y_formation,
    line=dict(width=2, color='black'),
    hoverinfo='none',
    mode='lines'
)

# Add annotations for formation
center_x, center_y = pos_formation[0]
edge_x, edge_y = pos_formation[1]
mid_x = (center_x + edge_x) / 2
mid_y = (center_y + edge_y) / 2

# Add traces to the formation subplot
fig.add_trace(edge_trace_formation, row=1, col=1)
fig.add_trace(node_trace_formation, row=1, col=1)

# Add annotation for edges
fig.add_annotation(
    x=mid_x,
    y=mid_y,
    text="Edge (Distance)",
    showarrow=True,
    arrowhead=2,
    arrowsize=1,
    arrowwidth=2,
    arrowcolor="red",
    ax=-40,
    ay=-40,
    row=1, col=1,
    font=dict(color="red", size=12)
)

# Add annotation for node
fig.add_annotation(
    x=edge_x,
    y=edge_y,
    text="Node (Temperature and Rainfall)",
    showarrow=True,
    arrowhead=2,
    arrowsize=1,
    arrowwidth=2,
    arrowcolor="red",
    ax=40,
    ay=40,
    row=1, col=1,
    font=dict(color="red", size=12)
)

# ===== GCN VISUALIZATION (BOTTOM) =====
# Create initial graph (with striped nodes)
G_initial = nx.star_graph(8)
pos_initial = nx.spring_layout(G_initial, seed=42)  # Use same seed for consistency

# Create transformed graph (with solid nodes)
G_transformed = nx.star_graph(8)
pos_transformed = {node: (x + 1.5, y) for node, (x, y) in pos_initial.items()}  # Shift right

# Create node trace for initial graph
node_x_initial = []
node_y_initial = []
for node in G_initial.nodes():
    x, y = pos_initial[node]
    node_x_initial.append(x)
    node_y_initial.append(y)

node_trace_initial = go.Scatter(
    x=node_x_initial,
    y=node_y_initial,
    mode='markers',
    marker=dict(
        size=20,
        color=['white' if node == 0 else 'white' for node in G_initial.nodes()],
        line=dict(width=2, color='black'),
        symbol='circle-open-dot'  # This gives a striped appearance
    ),
    text=[f"Node {i}" for i in G_initial.nodes()],
    hoverinfo='text'
)

# Create edge trace for initial graph
edge_x_initial = []
edge_y_initial = []
for edge in G_initial.edges():
    x0, y0 = pos_initial[edge[0]]
    x1, y1 = pos_initial[edge[1]]
    edge_x_initial.extend([x0, x1, None])
    edge_y_initial.extend([y0, y1, None])

edge_trace_initial = go.Scatter(
    x=edge_x_initial,
    y=edge_y_initial,
    line=dict(width=2, color='black'),
    hoverinfo='none',
    mode='lines'
)

# Create node trace for transformed graph
node_x_transformed = []
node_y_transformed = []
for node in G_transformed.nodes():
    x, y = pos_transformed[node]
    node_x_transformed.append(x)
    node_y_transformed.append(y)

node_trace_transformed = go.Scatter(
    x=node_x_transformed,
    y=node_y_transformed,
    mode='markers',
    marker=dict(
        size=20,
        color=['pink' if node == 0 else 'blue' for node in G_transformed.nodes()],
        line=dict(width=2, color='black')
    ),
    text=[f"Node {i}" for i in G_transformed.nodes()],
    hoverinfo='text'
)

# Create edge trace for transformed graph
edge_x_transformed = []
edge_y_transformed = []
for edge in G_transformed.edges():
    x0, y0 = pos_transformed[edge[0]]
    x1, y1 = pos_transformed[edge[1]]
    edge_x_transformed.extend([x0, x1, None])
    edge_y_transformed.extend([y0, y1, None])

edge_trace_transformed = go.Scatter(
    x=edge_x_transformed,
    y=edge_y_transformed,
    line=dict(width=2, color='black'),
    hoverinfo='none',
    mode='lines'
)

# Add traces to the GCN subplot
fig.add_trace(edge_trace_initial, row=2, col=1)
fig.add_trace(node_trace_initial, row=2, col=1)
fig.add_trace(edge_trace_transformed, row=2, col=1)
fig.add_trace(node_trace_transformed, row=2, col=1)

# Add GCN arrow
fig.add_annotation(
    x=0.5, y=0.5,
    xref="paper", yref="paper",
    text="GCN",
    showarrow=True,
    arrowhead=1,
    arrowsize=1.5,
    arrowwidth=2,
    ax=0,
    ay=0,
    font=dict(size=16),
    row=2, col=1
)

# Add message aggregation function as a rect instead of ellipse
# We'll use a rect with rounded corners to simulate an oval shape
fig.add_shape(
    type="rect",  # Using rect instead of ellipse (which is not supported)
    xref="x", yref="y",
    x0=-0.2, y0=-1.5, x1=1.7, y1=-0.8,
    line_color="black",
    fillcolor="white",
    row=2, col=1
)

# Add message aggregation function text
fig.add_annotation(
    x=0.75, y=-1.15,
    text="Message Aggregation Function + Update Function",
    showarrow=False,
    font=dict(size=14),
    row=2, col=1
)

# Add arrow from GCN to message function
fig.add_annotation(
    x=0.75, y=-0.5,
    text="",
    showarrow=True,
    arrowhead=1,
    arrowsize=1.5,
    arrowwidth=2,
    ax=0,
    ay=-50,
    row=2, col=1
)

# Update layout
fig.update_layout(
    showlegend=False,
    height=800,
    margin=dict(b=20, l=5, r=5, t=60),
    plot_bgcolor='rgb(248,248,248)'
)

# Update xaxes and yaxes
for i in range(1, 3):
    fig.update_xaxes(showgrid=False, zeroline=False, showticklabels=False, row=i, col=1)
    fig.update_yaxes(showgrid=False, zeroline=False, showticklabels=False, row=i, col=1)

# Show figure
fig.show()

# To save the figure as an HTML file (for interactivity):
# fig.write_html("graph_formation_and_gcn.html")
