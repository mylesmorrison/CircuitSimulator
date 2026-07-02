import numpy as np
from core.components import VoltageSource

GROUND_NAMES = {"GND", "0"}

def solve(components):
    """Solve a circuit. Returns (voltages_dict, source_currents_dict)."""

    # --- Step 1: discover nodes ---
    node_names = set()
    for comp in components:
        node_names.update(comp.nodes)
    node_names -= GROUND_NAMES

    if not node_names:
        raise ValueError("Circuit has no non-ground nodes")

    # --- Step 2: assign indices ---
    node_index = {name: i for i, name in enumerate(sorted(node_names))}

    vsources = [c for c in components if isinstance(c, VoltageSource)]
    for k, vs in enumerate(vsources):
        vs.current_index = len(node_index) + k

    # --- Step 3: build and stamp ---
    n = len(node_index) + len(vsources)
    G = np.zeros((n, n))
    b = np.zeros(n)

    for comp in components:
        comp.stamp(G, b, node_index)

    # --- Step 4: solve and map back ---
    try:
        x = np.linalg.solve(G, b)
    except np.linalg.LinAlgError:
        raise ValueError(
            "Singular matrix — check for floating nodes or "
            "misspelled node names"
        )

    voltages = {name: x[i] for name, i in node_index.items()}
    for g in GROUND_NAMES:
        voltages[g] = 0.0

    currents = {vs.id: x[vs.current_index] for vs in vsources}
    return voltages, currents