class Cluster:
    def __init__(self):
        self.nodes = []

    def add_node(self, node):
        self.nodes.append(node)

    def fail_node(self, node_id):
        node = next((node for node in self.nodes if node.node_id == node_id), None)
        if node:
            node.fail()