import socket
import threading
import json
import time
import sys

import sys

if len(sys.argv) < 2:

    print(
        "Usage: python src/node.py <node_id>"
    )

    sys.exit()

NODE_ID = int(sys.argv[1])

NODES = {
    1: ("localhost", 7001),
    2: ("localhost", 7002),
    3: ("localhost", 7003),
    4: ("localhost", 7004),
    5: ("localhost", 7005),
}

LEADER = 5

class Node:
    
    def __init__(self, node_id):

        self.node_id = node_id

        self.host, self.port = NODES[node_id]

    def start(self):

        server = socket.socket(
            socket.AF_INET,
            socket.SOCK_STREAM
        )

        server.setsockopt(
            socket.SOL_SOCKET,
            socket.SO_REUSEADDR,
            1
        )

        server.bind(
            (self.host, self.port)
        )

        server.listen()

        print(
            f"Node {self.node_id} listening on {self.host}:{self.port}"
        )

        while True:

            conn, addr = server.accept()

            threading.Thread(
                target=self.handle_client,
                args=(conn,),
                daemon=True
            ).start()

    def is_alive(self, node_id):

        host, port = NODES[node_id]

        try:

            sock = socket.socket(
                socket.AF_INET,
                socket.SOCK_STREAM
            )

            sock.settimeout(1)

            sock.connect(
                (host, port)
            )

            sock.close()

            return True

        except:

            return False

    def handle_client(self, conn):

        try:

            data = conn.recv(4096)

            if not data:
                return

            message = json.loads(
                data.decode()
            )

            msg_type = message["type"]

            if msg_type == "TRANSACTION":

                self.handle_transaction(
                    message["transaction"]
                )

            elif msg_type == "PREPARE":

                print(
                    f"Node {self.node_id} -> PROMISE"
                )

            elif msg_type == "ACCEPT":

                print(
                    f"Node {self.node_id} -> ACCEPTED"
                )

        finally:

            conn.close()

    def send_message(
        self,
        target_node,
        payload
    ):

        host, port = NODES[target_node]

        try:

            sock = socket.socket(
                socket.AF_INET,
                socket.SOCK_STREAM
            )

            sock.connect(
                (host, port)
            )

            sock.send(
                json.dumps(payload).encode()
            )

            sock.close()

        except Exception as e:

            print(
                f"Communication Error: {e}"
            )

    def handle_transaction(
        self,
        transaction
    ):

        if self.node_id != LEADER:
            return

        print("\n")
        print(
            f"Leader Node {LEADER} received transaction:"
        )
        print(transaction)

        print("\nPAXOS PREPARE PHASE")
        print("-------------------")

        alive_nodes = []

        for node in NODES:

            if node == LEADER:
                continue

            if self.is_alive(node):

                alive_nodes.append(node)

        print(
            f"Alive Nodes: {alive_nodes}"
        )

        for node in alive_nodes:

            print(
                f"Leader -> Node {node} : PREPARE"
            )

            self.send_message(
                node,
                {
                    "type": "PREPARE"
                }
            )

            time.sleep(0.5)

        print("\nPAXOS ACCEPT PHASE")
        print("------------------")

        accepted = 0

        for node in alive_nodes:

            print(
                f"Leader -> Node {node} : ACCEPT"
            )

            self.send_message(
                node,
                {
                    "type": "ACCEPT"
                }
            )

            accepted += 1

            time.sleep(0.5)

        print("\nCONSENSUS RESULT")
        print("----------------")

        majority = (len(alive_nodes) + 1) // 2

        if accepted >= majority:

            print(
                "Majority Reached"
            )

            print(
                "Transaction COMMITTED"
            )

        else:

            print(
                "Consensus Failed"
            )

    def heartbeat(self):

        global LEADER

        while True:

            try:

                host, port = NODES[LEADER]

                sock = socket.socket(
                    socket.AF_INET,
                    socket.SOCK_STREAM
                )

                sock.settimeout(1)

                sock.connect(
                    (host, port)
                )

                sock.close()

                print(
                    f"[Heartbeat] Leader Node {LEADER} Alive"
                )

            except:

                print(
                    f"[Heartbeat] Leader Node {LEADER} Unreachable"
                )

                self.elect_leader()

            time.sleep(5)
            
    def elect_leader(self):

        global LEADER

        alive_nodes = []

        for node_id in NODES:

            if self.is_alive(node_id):

                alive_nodes.append(node_id)

        if alive_nodes:

            new_leader = max(alive_nodes)

            if new_leader != LEADER:

                print(
                    f"\nLeader Failure Detected!"
                )

                print(
                    f"New Leader Elected: Node {new_leader}"
                )

                LEADER = new_leader
                
if __name__ == "__main__":
    alive_nodes = []

    for node_id in NODES:

        try:

            host, port = NODES[node_id]

            sock = socket.socket(
                socket.AF_INET,
                socket.SOCK_STREAM
            )

            sock.settimeout(1)

            sock.connect(
                (host, port)
            )

            sock.close()

            alive_nodes.append(node_id)

        except:

            pass

    if alive_nodes:

        LEADER = max(alive_nodes)

    print(
        f"Current Leader = Node {LEADER}"
    )
    node = Node(NODE_ID)

    threading.Thread(
        target=node.heartbeat,
        daemon=True
    ).start()

    node.start()

    while True:

        time.sleep(1)