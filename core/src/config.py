"""
Central configuration and canonical system contract for the 5-node migration.
"""

from __future__ import annotations

import math
from typing import Dict, List

import pandas as pd
import torch

# ---------------------------------------------------------------------------
# Canonical data/model contract
# ---------------------------------------------------------------------------
OPEN_METEO_MODEL = "era5"
GRAPH_TOPOLOGY = "star"
TARGET_NODE_POLICY = "main_node_only"
CONTEXT_POLICY = "main_node_context"

# Node order is mandatory and must be stable across ingestion, loader, training,
# checkpoint, inference, and evaluation.
NODE_DEFINITIONS: List[Dict[str, object]] = [
    {
        "name": "MAIN",
        "role": "main",
        "alias": "Puncak",
        "lat": -6.75,
        "lon": 107.00,
        "elevation_m": 1529.0,
    },
    {
        "name": "UP",
        "role": "surrounding",
        "alias": "Up",
        "lat": -6.50,
        "lon": 107.00,
        "elevation_m": 162.0,
    },
    {
        "name": "DOWN",
        "role": "surrounding",
        "alias": "Down",
        "lat": -7.00,
        "lon": 107.00,
        "elevation_m": 0.0,
    },
    {
        "name": "LEFT",
        "role": "surrounding",
        "alias": "Left",
        "lat": -6.75,
        "lon": 106.75,
        "elevation_m": 823.0,
    },
    {
        "name": "RIGHT",
        "role": "surrounding",
        "alias": "Right",
        "lat": -6.75,
        "lon": 107.25,
        "elevation_m": 288.0,
    },
]

NODE_NAMES = [node["name"] for node in NODE_DEFINITIONS]
NODE_ROLES = {node["name"]: node["role"] for node in NODE_DEFINITIONS}
NODE_COORDINATES = {node["name"]: (float(node["lat"]), float(node["lon"])) for node in NODE_DEFINITIONS}
NODE_ELEVATIONS = {node["name"]: float(node["elevation_m"]) for node in NODE_DEFINITIONS}
NUM_NODES = len(NODE_DEFINITIONS)

MAIN_NODE_NAME = "MAIN"
MAIN_NODE_IDENTIFIER = NODE_COORDINATES[MAIN_NODE_NAME]

STAR_EDGES = [
    (MAIN_NODE_NAME, "UP"),
    ("UP", MAIN_NODE_NAME),
    (MAIN_NODE_NAME, "DOWN"),
    ("DOWN", MAIN_NODE_NAME),
    (MAIN_NODE_NAME, "LEFT"),
    ("LEFT", MAIN_NODE_NAME),
    (MAIN_NODE_NAME, "RIGHT"),
    ("RIGHT", MAIN_NODE_NAME),
]
STAR_EDGE_COUNT = len(STAR_EDGES)

FINAL_TARGET_COLS = [
    "precipitation",
    "wind_speed",
    "relative_humidity",
]

# Physical upper bound for hourly precipitation (mm/h). Dataset max ~21.5; this generous
# cap is numerical hygiene only (prevents expm1 blow-up on out-of-distribution inputs),
# well above any real value so it never distorts healthy predictions.
PRECIP_PHYSICAL_MAX_MM = 60.0

# Shared numerical hygiene constants (single source; previously duplicated literals).
ZSCORE_EPSILON = 1e-5
DDIM_INFERENCE_STEPS = 20

# Diffusion training horizon (number of noising steps). Must match between the
# training-time random timestep draw and both schedulers.
DIFFUSION_TRAIN_TIMESTEPS = 1000

# Log-space ceiling applied before expm1 when converting predicted precipitation
# back to mm/h. Protects against overflow (e^20 ~ 4.85e8); NOT a physical bound —
# that is PRECIP_PHYSICAL_MAX_MM above.
LOG_PRECIP_MAX = 20.0

# Heavy-rain event definition used by all probabilistic skill scores.
HEAVY_RAIN_THRESHOLD_MM = 10.0
PROB_EVENT_THRESHOLD = 0.5

FINAL_FEATURE_COLS = [
    "temperature",
    "relative_humidity",
    "dewpoint",
    "surface_pressure",
    "wind_speed",
    "wind_direction",
    "cloud_cover",
    "precipitation_lag1",
    "elevation",
]

# PDF Sec 3.4.2 (p059) + Tabel 3.5 (p059-p060): harmonisation strips the
# measurement-height suffix (_2m/_10m) from the analysis names, keeping the API
# field name as the source key.
OPTIONAL_LEGACY_RENAMES = {
    "temperature_2m": "temperature",
    "relative_humidity_2m": "relative_humidity",
    "dew_point_2m": "dewpoint",
    "dewpoint_2m": "dewpoint",
    "wind_speed_10m": "wind_speed",
    "wind_direction_10m": "wind_direction",
    "cloudcover": "cloud_cover",
}


def harmonize_weather_columns(df: pd.DataFrame) -> pd.DataFrame:
    """
    Normalize legacy column names to the final contract used by the pipeline.
    """
    rename_map = {old: new for old, new in OPTIONAL_LEGACY_RENAMES.items() if old in df.columns}
    if rename_map:
        df = df.rename(columns=rename_map)
    return df


def validate_feature_schema(df: pd.DataFrame, feature_cols=None, target_cols=None) -> None:
    """
    Raise a clear error when the dataset does not match the required contract.
    """
    feature_cols = feature_cols or FINAL_FEATURE_COLS
    target_cols = target_cols or FINAL_TARGET_COLS
    missing = [col for col in [*feature_cols, *target_cols] if col not in df.columns]
    if missing:
        raise ValueError(f"Dataset schema mismatch. Missing required columns: {missing}")


def validate_feature_values(df: pd.DataFrame, feature_cols=None) -> None:
    """
    Raise an error if a required feature exists in schema but contains no usable values.
    """
    feature_cols = feature_cols or FINAL_FEATURE_COLS
    invalid = [col for col in feature_cols if col in df.columns and df[col].notna().sum() == 0]
    if invalid:
        raise ValueError(f"Dataset contains required features with all-NaN values: {invalid}")


def get_node_dataframe() -> pd.DataFrame:
    """
    Return canonical node table in mandatory order.
    """
    return pd.DataFrame(NODE_DEFINITIONS).copy()


def get_node_index_map(node_names: List[str] | None = None) -> Dict[str, int]:
    """
    Return node -> index mapping for stable tensor order.
    """
    names = node_names or NODE_NAMES
    return {name: i for i, name in enumerate(names)}


def build_star_edge_index(node_names: List[str] | None = None) -> torch.Tensor:
    """
    Build canonical star edge index in directed form.
    """
    names = node_names or NODE_NAMES
    idx = get_node_index_map(names)
    missing = sorted({name for edge in STAR_EDGES for name in edge if name not in idx})
    if missing:
        raise ValueError(f"Cannot build star edges. Missing nodes: {missing}")
    sources = [idx[src] for src, _ in STAR_EDGES]
    targets = [idx[dst] for _, dst in STAR_EDGES]
    edge_index = torch.tensor([sources, targets], dtype=torch.long)
    if edge_index.shape[1] != STAR_EDGE_COUNT:
        raise ValueError(
            f"Star edge count mismatch. Expected {STAR_EDGE_COUNT}, got {edge_index.shape[1]}"
        )
    return edge_index


EARTH_RADIUS_KM = 6371.0088


def haversine_km(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """Great-circle distance between two lat/lon points, in kilometres."""
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    dphi = phi2 - phi1
    dlambda = math.radians(lon2 - lon1)
    a = math.sin(dphi / 2.0) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(dlambda / 2.0) ** 2
    return 2.0 * EARTH_RADIUS_KM * math.asin(min(1.0, math.sqrt(a)))


def build_star_edge_attr(node_names: List[str] | None = None) -> torch.Tensor:
    """
    Build static per-edge attributes for the star graph. Shape: [num_edges, 2].

    Features, per directed edge (u, v):
      [0] haversine distance u->v in km (normalised by the star radius),
      [1] heavy-tail transform 1/(1 + d/d_ref), bounded in (0, 1].

    NOTE (honest limitation): on the canonical 0.25-deg grid every surrounding node sits
    ~27.6-27.8 km from MAIN, so a *constant* edge attribute collapses the whole GATConv
    edge branch to one learnable scalar per attention head (verified: zero reproduction
    error against a manual forward). The two features below still separate radial (N/S vs
    E/W) from latency, which a single scalar could not. Elevation difference was tested and
    empirically degraded training convergence, so it is retained per node (NODE_ELEVATIONS)
    rather than injected as an edge weight.
    """
    names = node_names or NODE_NAMES
    d_ref = max(
        1e-6,
        max(
            haversine_km(*NODE_COORDINATES[MAIN_NODE_NAME], *NODE_COORDINATES[name])
            for name in names
            if name != MAIN_NODE_NAME and name in NODE_COORDINATES
        ),
    )
    rows = []
    for src, dst in STAR_EDGES:
        if src not in NODE_COORDINATES or dst not in NODE_COORDINATES:
            raise ValueError(f"Cannot build edge attr. Missing coordinates for edge {(src, dst)}")
        dist_km = haversine_km(*NODE_COORDINATES[src], *NODE_COORDINATES[dst])
        rows.append([dist_km / d_ref, 1.0 / (1.0 + dist_km / d_ref)])
    edge_attr = torch.tensor(rows, dtype=torch.float32)
    if edge_attr.shape[0] != STAR_EDGE_COUNT:
        raise ValueError(
            f"Star edge attr count mismatch. Expected {STAR_EDGE_COUNT}, got {edge_attr.shape[0]}"
        )
    return edge_attr


def get_checkpoint_node_metadata() -> Dict[str, object]:
    """
    Metadata block that must be stored in model checkpoints.
    """
    return {
        "node_names": list(NODE_NAMES),
        "node_roles": dict(NODE_ROLES),
        "node_coordinates": dict(NODE_COORDINATES),
        "main_node_identifier": MAIN_NODE_IDENTIFIER,
        "main_node_name": MAIN_NODE_NAME,
        "graph_topology": GRAPH_TOPOLOGY,
        "num_nodes": NUM_NODES,
        "target_node_policy": TARGET_NODE_POLICY,
        "context_policy": CONTEXT_POLICY,
        "star_edges": list(STAR_EDGES),
    }

