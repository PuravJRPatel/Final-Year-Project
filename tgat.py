import torch
import torch.nn as nn
import torch.nn.functional as F
import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
from torch_geometric.nn import GATConv, global_mean_pool
from torch_geometric.data import Data, Batch

# Step 1: Input Temporal Data
def create_temporal_data(num_nodes, num_timesteps, in_channels):
    return torch.rand((num_nodes, num_timesteps, in_channels))  # Temporal features

# Step 2: Graph Construction
def create_graph(num_nodes):
    edge_index = torch.randint(0, num_nodes, (2, num_nodes * 2))  # Random edges
    return edge_index

# Visualize the graph
def visualize_graph(edge_index, num_nodes, title="Spatial Graph Visualization"):
    G = nx.Graph()
    G.add_nodes_from(range(num_nodes))
    edges = edge_index.t().tolist()
    G.add_edges_from(edges)

    # Draw the graph
    plt.figure(figsize=(8, 6))
    pos = nx.spring_layout(G, seed=42)
    nx.draw(G, pos, with_labels=True, node_color='skyblue', node_size=500, edge_color='gray')
    plt.title(title)
    plt.show()

# Step 3: Spatial Graph Attention Network (GAT)
class SpatialGAT(nn.Module):
    def __init__(self, in_channels, hidden_channels):
        super(SpatialGAT, self).__init__()
        self.gat1 = GATConv(in_channels, hidden_channels, heads=4, concat=True)
        self.gat2 = GATConv(hidden_channels * 4, hidden_channels, heads=1, concat=False)

    def forward(self, x, edge_index):
        x = F.relu(self.gat1(x, edge_index))
        x = F.relu(self.gat2(x, edge_index))
        return x

# Step 4: Temporal Graph Convolution (TGNN)
class TemporalGNN(nn.Module):
    def __init__(self, hidden_channels):
        super(TemporalGNN, self).__init__()
        self.lstm = nn.LSTM(hidden_channels, hidden_channels, batch_first=True)

    def forward(self, x):
        lstm_out, (h_n, c_n) = self.lstm(x)
        return lstm_out[:, -1, :]  # Last time step output

# Step 5: Fully Connected Layer
class FullyConnected(nn.Module):
    def __init__(self, hidden_channels, out_channels):
        super(FullyConnected, self).__init__()
        self.fc = nn.Linear(hidden_channels, out_channels)

    def forward(self, x):
        return self.fc(x)

# Final Model: Combining Spatial and Temporal Analysis
class SeaSurfaceTemperatureModel(nn.Module):
    def __init__(self, in_channels, hidden_channels, out_channels, num_timesteps):
        super(SeaSurfaceTemperatureModel, self).__init__()
        self.spatial_gat = SpatialGAT(in_channels, hidden_channels)
        self.temporal_gnn = TemporalGNN(hidden_channels)
        self.fc = FullyConnected(hidden_channels, out_channels)
        self.num_timesteps = num_timesteps

    def forward(self, temporal_data, edge_index, batch):
        num_nodes = temporal_data.size(0)
        x = temporal_data.view(num_nodes * self.num_timesteps, -1)  # Flatten temporal features
        x = self.spatial_gat(x, edge_index)  # Spatial GAT
        x = x.view(num_nodes, self.num_timesteps, -1)  # Reshape for LSTM
        x = self.temporal_gnn(x)  # Temporal GNN
        x = global_mean_pool(x, batch)  # Pooling
        output = self.fc(x)  # Fully Connected Layer
        return output

# Hyperparameters
num_nodes = 25
num_timesteps = 50
in_channels = 16
hidden_channels = 32
out_channels = 1

# Generate Synthetic Data
temporal_data = create_temporal_data(num_nodes, num_timesteps, in_channels)
edge_index = create_graph(num_nodes)
batch = torch.zeros(num_nodes, dtype=torch.long)

# Visualize Graph
visualize_graph(edge_index, num_nodes, title="Spatial Graph of Nodes")

# Instantiate and Run Model
model = SeaSurfaceTemperatureModel(in_channels, hidden_channels, out_channels, num_timesteps)
output = model(temporal_data, edge_index, batch)

# Display Prediction Output
print("Predicted Average Sea Surface Temperature (SST):", output.item())

# Spatial Visualization of Predictions
node_temperatures = torch.rand(num_nodes)  # Simulate node temperature predictions
node_positions = np.random.rand(num_nodes, 2)  # Random positions for nodes

plt.figure(figsize=(8, 6))
plt.scatter(node_positions[:, 0], node_positions[:, 1], c=node_temperatures, cmap='coolwarm', s=200)
plt.colorbar(label="Predicted Node Temperatures")
plt.title("Spatial Visualization of Predicted SST at Nodes")
plt.xlabel("X Position")
plt.ylabel("Y Position")
plt.show()

# Temporal Visualization: Simulate SST Progression
time_steps = np.arange(1, num_timesteps + 1)
average_temps = torch.mean(temporal_data, dim=(0, 2))  # Average across nodes and features

plt.figure(figsize=(10, 6))
plt.plot(time_steps, average_temps.numpy(), color='dodgerblue', linewidth=2)
plt.title("Temporal Progression of Average Sea Surface Temperature")
plt.xlabel("Time Steps")
plt.ylabel("Average SST")
plt.grid(True)
plt.show()
