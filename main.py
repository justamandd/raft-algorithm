from node import Node
from cluster import Cluster
import time
import random

def main():
    cluster = Cluster()
    nodes = [Node(i, cluster) for i in range(5)]

    for node in nodes:
        cluster.add_node(node)
        node.start()

    try:
        while True:
            time.sleep(random.uniform(3, 5))

            for node in nodes:
                node.log_status()

            if random.random() < 0.3:
                node_to_fail = random.choice(nodes)
                if not node_to_fail.failed:
                    cluster.fail_node(node_to_fail.node_id)

            if random.random() < 0.2:
                for node in nodes:
                    if node.failed:
                        node.recover()

    except KeyboardInterrupt:
        print("Encerrando o programa.")

if __name__ == "__main__":
    main()
