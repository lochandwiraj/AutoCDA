import networkx as nx
from typing import Dict, List, Tuple

class NetlistGraph:
    def __init__(self):
        self.graph = nx.Graph()
        self.components = {}
        self.nets = {}
    
    def add_component(self, id: str, type: str, value: str, nets: List[str]):
        """Add component to graph"""
        self.components[id] = {"type": type, "value": value, "nets": nets}
        
        # Add nodes for nets if not exist
        for net in nets:
            if net not in self.graph:
                self.graph.add_node(net, node_type="net")
        
        # Add edges between nets through this component
        for i in range(len(nets)):
            for j in range(i+1, len(nets)):
                self.graph.add_edge(nets[i], nets[j], 
                                   component=id, 
                                   comp_type=type)
    
    def find_floating_nodes(self) -> List[str]:
        """Find nets with no ground connection"""
        if "GND" not in self.graph:
            return []
        
        connected_to_gnd = nx.node_connected_component(self.graph, "GND")
        all_nets = set(self.graph.nodes())
        return list(all_nets - connected_to_gnd)
    
    def detect_voltage_dividers(self) -> List[Dict]:
        """Detect resistor divider patterns"""
        dividers = []
        
        # Look for two resistors in series between two nets
        for node in self.graph.nodes():
            neighbors = list(self.graph.neighbors(node))
            
            # Check if this node connects exactly 2 resistors
            connected_resistors = []
            for neighbor in neighbors:
                edge_data = self.graph.get_edge_data(node, neighbor)
                if edge_data and edge_data.get('comp_type') == 'resistor':
                    connected_resistors.append(edge_data['component'])
            
            if len(connected_resistors) == 2:
                dividers.append({
                    "middle_node": node,
                    "resistors": connected_resistors
                })
        
        return dividers
    
    def visualize(self, output_path: str = "circuit_graph.png"):
        """Draw the circuit graph"""
        import matplotlib.pyplot as plt
        
        pos = nx.spring_layout(self.graph)
        nx.draw(self.graph, pos, with_labels=True, 
                node_color='lightblue', node_size=1500,
                font_size=10, font_weight='bold')
        
        plt.savefig(output_path)
        plt.close()