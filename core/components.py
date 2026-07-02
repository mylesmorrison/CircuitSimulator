class Component:
    def __init__(self, comp_id, value, nodes):
        self.id = comp_id
        self.nodes = nodes
        self.value = value

    def stamp(self):
        raise NotImplementedError

class Resistor(Component):
    def stamp(self, G, b, node_index):
        g = 1.0 / self.value
        i = node_index.get(self.nodes[0])
        j = node_index.get(self.nodes[1])

        if i is not None:
            G[i, i] += g
        if j is not None:
            G[j, j] += g
        if i is not None and j is not None:
            G[i, j] -= g
            G[j, i] -= g

class VoltageSource(Component):
    def __init__(self, comp_id: str, value: float, nodes: list[str]):
        super().__init__(comp_id, value, nodes)
        self.current_index = None  # assigned by the solver before stamping

    def stamp(self, G, b, node_index):
        k = self.current_index
        pos = node_index.get(self.nodes[0])
        neg = node_index.get(self.nodes[1])

        if pos is not None:
            G[pos, k] += 1
            G[k, pos] += 1
        if neg is not None:
            G[neg, k] -= 1
            G[k, neg] -= 1
        b[k] += self.value

