import socket
import json

NODES = {
    5: ("localhost", 7005),
    4: ("localhost", 7004),
    3: ("localhost", 7003),
    2: ("localhost", 7002),
    1: ("localhost", 7001),
}

transaction = input(
    "Enter Transaction: "
)

payload = {
    "type": "TRANSACTION",
    "transaction": transaction
}

leader_found = False

for node_id in NODES:

    host, port = NODES[node_id]

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

        print()
        print(
            f"Transaction sent to Leader Node {node_id}"
        )

        leader_found = True

        break

    except:

        continue

if not leader_found:

    print(
        "No active leader found"
    )