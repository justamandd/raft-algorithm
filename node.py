import random
import time
import threading

class Node:
    def __init__(self, node_id, cluster):
        self.node_id = node_id
        self.state = "follower"
        self.term = 0
        self.votes_received = 0
        self.cluster = cluster
        self.value = node_id + 1
        self.election_timeout = random.uniform(2, 3)
        self.heartbeat_timeout = 1.0
        self.vote_granted = False
        self.lock = threading.Lock()
        self.failed = False

    def start(self):
        threading.Thread(target=self.run, daemon=True).start()

    def run(self):
        while True:
            if self.failed:
                time.sleep(random.uniform(5, 7))
                self.recover()
            elif self.state == "follower":
                self.follow_leader()
            elif self.state == "candidate":
                self.run_for_election()
            elif self.state == "leader":
                self.lead()

    def follow_leader(self):
        time.sleep(self.election_timeout)
        if not self.vote_granted:
            self.state = "candidate"
            self.log_status()

    def run_for_election(self):
        self.term += 1
        self.votes_received = 1
        self.vote_granted = False

        for node in self.cluster.nodes:
            if node.node_id != self.node_id and not node.failed:
                node.receive_vote_request(self)

        time.sleep(self.election_timeout)
        if self.votes_received > len(self.cluster.nodes) // 2:
            self.state = "leader"
            self.broadcast_value()

        self.log_status()

    def receive_vote_request(self, candidate):
        with self.lock:
            if self.state == "follower" and candidate.term > self.term and not self.failed:
                self.term = candidate.term
                self.state = "follower"
                self.vote_granted = True
                candidate.votes_received += 1

    def lead(self):
        while self.state == "leader" and not self.failed:
            time.sleep(self.heartbeat_timeout)
            self.term += 1
            self.value += 1
            self.broadcast_value()
            self.log_status()

    def broadcast_value(self):
        print(f"** LÍDER {self.node_id} ** Atualizando Valor para {self.value} e Termo {self.term}")
        for node in self.cluster.nodes:
            if node.node_id != self.node_id and not node.failed:
                print(f"  ** Propagando Valor {self.value} e Termo {self.term} para Nó {node.node_id}")
                node.receive_value(self.value, self.term)

    def receive_value(self, value, term):
        with self.lock:
            if term >= self.term:
                print(f"  ** Nó {self.node_id} recebeu o valor {value} e termo {term} do líder.")
                self.term = term
                self.value = value

    def fail(self):
        self.failed = True

    def recover(self):
        self.failed = False
        self.state = "follower"
        self.term += 1
        self.votes_received = 0
        self.vote_granted = False
        self.sync_value_with_leader()

    def sync_value_with_leader(self):
        leader = self.find_leader()
        if leader:
            with self.lock:
                self.value = leader.value
                self.term = leader.term

    def find_leader(self):
        for node in self.cluster.nodes:
            if node.state == "leader" and not node.failed:
                return node
        return None

    def log_status(self):
        print(f"\n--- Status do No {self.node_id} ---")
        print(f"Estado = {self.state}, Termo = {self.term}, Valor = {self.value}, Falhou = {self.failed}")
        print(f"\n--- Nova Iteração ---")