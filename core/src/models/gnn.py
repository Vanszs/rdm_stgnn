"""
Spatio-Temporal Graph Neural Network Module.

Canonical context:
- 5-node star graph (MAIN, UP, DOWN, LEFT, RIGHT)
- Temporal sequence conditioning for diffusion forecasting
"""

import torch
import torch.nn as nn
from torch_geometric.nn import GATConv, global_mean_pool


class TemporalAttention(nn.Module):
    """
    Self-attention layer for temporal sequence modeling.
    Learns which past timesteps are most relevant for prediction.
    """
    def __init__(self, hidden_dim, num_heads=4, dropout=0.1, max_len=64, causal=True):
        super().__init__()
        self.max_len = int(max_len)
        self.causal = bool(causal)
        self.attention = nn.MultiheadAttention(
            embed_dim=hidden_dim,
            num_heads=num_heads,
            dropout=dropout,
            batch_first=True
        )
        self.norm = nn.LayerNorm(hidden_dim)
        self.dropout = nn.Dropout(dropout)
        self.pos_embedding = nn.Parameter(torch.zeros(1, self.max_len, hidden_dim))
        nn.init.normal_(self.pos_embedding, mean=0.0, std=0.02)

        # Learned-query pooling: ONE query attends over all timesteps, so the output is a
        # fixed-size [Batch, Hidden_Dim] embedding with no dependency on seq_len (unlike
        # slicing x[:, -1, :], which discards every other timestep).
        self.pool_query = nn.Parameter(torch.empty(1, 1, hidden_dim))
        nn.init.normal_(self.pool_query, mean=0.0, std=0.02)

    def forward(self, x):
        """
        x: [Batch, Seq_Len, Hidden_Dim]
        Returns: [Batch, Hidden_Dim] (learned pooling over ALL timesteps)
        """
        seq_len = x.shape[1]
        if seq_len > self.max_len:
            raise ValueError(
                f"TemporalAttention sequence length {seq_len} exceeds max_len={self.max_len}"
            )

        # Add positional encoding to keep timestep order identifiable.
        x = x + self.pos_embedding[:, :seq_len, :]

        # Causal mask ensures timestep t cannot attend to future timesteps > t.
        attn_mask = torch.triu(
            torch.ones(seq_len, seq_len, device=x.device, dtype=torch.bool),
            diagonal=1,
        )

        # Self-attention
        attn_out, _ = self.attention(x, x, x, attn_mask=attn_mask)
        x = self.norm(x + self.dropout(attn_out))

        # Pool the full sequence with a learned query. Causal self-attention already
        # stopped timestep t from seeing the future, so the pooled vector aggregates the
        # whole window without breaking temporality.
        query = self.pool_query.expand(x.shape[0], -1, -1)
        pooled, _ = self.attention(query, x, x)
        return pooled.squeeze(1)  # [Batch, Hidden_Dim]


class SpatialGNN(nn.Module):
    """
    Graph Attention Network for spatial dependencies across Gunung Gede-Pangrango nodes.
    Uses GAT to learn weighted message passing based on node features.

    `edge_dim=None` drops the edge branch entirely (GATConv then allocates no lin_edge /
    att_edge parameters). With a *constant* edge attribute that is the correct choice: the
    whole edge branch provably collapses to one learnable scalar per attention head
    (verified exactly, see build_star_edge_attr docstring) - i.e. the 640 edge-branch
    parameters of the edge_dim=1 config reduce to 5 free scalars (4 heads in conv1, 1 in
    conv2), and 4 of the 5 observed zero gradient in a training-path smoke check.
    """
    def __init__(self, input_dim, hidden_dim, output_dim, num_heads=4, edge_dim=2):
        super().__init__()

        # Two-layer GAT with edge attributes (haversine distance + heavy-tail transform).
        self.conv1 = GATConv(
            input_dim, hidden_dim, heads=num_heads, concat=True, dropout=0.1, edge_dim=edge_dim
        )
        self.conv2 = GATConv(
            hidden_dim * num_heads, output_dim, heads=1, concat=False, dropout=0.1, edge_dim=edge_dim
        )

        self.relu = nn.ReLU()

    def forward(self, x, edge_index, edge_attr=None, batch=None):
        """
        x: [Num_Nodes, Input_Dim]
        edge_index: [2, Num_Edges]
        edge_attr: [Num_Edges, Edge_Dim] or None when the edge branch is disabled
        batch: [Num_Nodes] - batch assignment for pooling
        """
        # Layer 1
        h = self.conv1(x, edge_index, edge_attr=edge_attr)
        h = self.relu(h)

        # Layer 2
        h = self.conv2(h, edge_index, edge_attr=edge_attr)

        # Global pooling to get graph-level representation
        if batch is not None:
            h = global_mean_pool(h, batch)  # [Batch, Output_Dim]

        return h


class SpatioTemporalGNN(nn.Module):
    """
    Combined Spatio-Temporal Graph Neural Network.
    
    Architecture:
    1. Spatial GNN processes each timestep's graph independently
    2. Temporal Attention aggregates across timesteps
    3. Output is a fixed-size graph embedding for conditioning diffusion
    
    This satisfies the "Spatio-Temporal Graph Conditioning" in thesis title.
    """
    def __init__(self, node_features, hidden_dim=64, output_dim=64,
                 num_gat_heads=4, num_attn_heads=4, seq_len=6, edge_dim=2):
        super().__init__()

        self.seq_len = seq_len
        self.hidden_dim = hidden_dim

        # Spatial component
        self.spatial_gnn = SpatialGNN(
            input_dim=node_features,
            hidden_dim=hidden_dim,
            output_dim=hidden_dim,
            num_heads=num_gat_heads,
            edge_dim=edge_dim,
        )
        
        # Temporal component
        self.temporal_attn = TemporalAttention(
            hidden_dim=hidden_dim,
            num_heads=num_attn_heads,
            max_len=seq_len,
            causal=True,
        )
        
        # Output projection
        self.output_proj = nn.Linear(hidden_dim, output_dim)
        
    def forward(self, graphs_sequence):
        """
        graphs_sequence: List of PyG Data objects, length = seq_len
                        Each Data has x=[Num_Nodes, Features], edge_index, etc.
        
        Returns: [Batch, Output_Dim] - Graph embedding for diffusion conditioning
        """
        # Process each timestep with spatial GNN
        spatial_outputs = []
        for graph in graphs_sequence:
            # graph.x: [Total_Nodes_In_Batch, Features]
            # graph.edge_index: [2, Total_Edges]
            # graph.edge_attr: [Total_Edges, Edge_Dim] - haversine edge attributes
            # graph.batch: [Total_Nodes] - identifies which sample each node belongs to
            edge_attr = getattr(graph, "edge_attr", None)
            h = self.spatial_gnn(graph.x, graph.edge_index, edge_attr=edge_attr, batch=graph.batch)
            spatial_outputs.append(h)
        
        # Stack temporal: [Batch, Seq_Len, Hidden_Dim]
        temporal_input = torch.stack(spatial_outputs, dim=1)
        
        # Aggregate temporal
        output = self.temporal_attn(temporal_input)  # [Batch, Hidden_Dim]
        
        # Project to output dim
        return self.output_proj(output)  # [Batch, Output_Dim]
