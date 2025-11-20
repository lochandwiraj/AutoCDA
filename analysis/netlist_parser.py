import networkx as nx
from typing import Dict, List

class NetlistGraph:
    def __init__(self):
        self.graph = nx.Graph()
        self.components = {}

    def add_component(self, id: str, type: str, value: str, nets: List[str]):
        self.components[id] = {"type": type, "value": value, "nets": nets}
        for net in nets:
            if net not in self.graph:
                self.graph.add_node(net, node_type="net")
        for i in range(len(nets)):
            for j in range(i+1, len(nets)):
                self.graph.add_edge(
                    nets[i],
                    nets[j],
                    component=id,
                    comp_type=type
                )

    def find_floating_nodes(self) -> List[str]:
        if "GND" not in self.graph:
            return []
        connected_to_gnd = nx.node_connected_component(self.graph, "GND")
        all_nets = set(self.graph.nodes())
        return list(all_nets - connected_to_gnd)

    def detect_voltage_dividers(self) -> List[Dict]:
        dividers = []
        for node in self.graph.nodes():
            neighbors = list(self.graph.neighbors(node))
            connected_resistors = []
            for neighbor in neighbors:
                edge_data = self.graph.get_edge_data(node, neighbor)
                if edge_data and edge_data.get("comp_type") == "resistor":
                    connected_resistors.append(edge_data["component"])
            if len(connected_resistors) == 2:
                dividers.append({
                    "middle_node": node,
                    "resistors": connected_resistors
                })
        return dividers
