import time
import threading

# -----------------------------------
# CLUSTER NODES
# -----------------------------------

nodes = [1, 2, 3, 4, 5]

leader = max(nodes)

leader_alive = True

# -----------------------------------
# HEARTBEAT MONITOR
# -----------------------------------

def heartbeat():

    global leader
    global leader_alive

    while True:

        print(f"[Heartbeat] Checking Leader Node {leader}")

        if not leader_alive:

            print("\nLeader Failure Detected!")

            if leader in nodes:
                nodes.remove(leader)

            leader = max(nodes)

            print(
                f"New Leader Elected: Node {leader}"
            )

            leader_alive = True

        time.sleep(3)

# Start heartbeat thread
heartbeat_thread = threading.Thread(
    target=heartbeat,
    daemon=True
)

heartbeat_thread.start()

# -----------------------------------
# INITIAL ELECTION
# -----------------------------------

print("Initial Election\n")

for node in nodes[:-1]:
    print(f"Node {node} is Follower")

print(f"Node {leader} is Leader")

time.sleep(5)

# -----------------------------------
# SIMULATE LEADER FAILURE
# -----------------------------------

print("\n")
print("Leader Crash")
print("----------------")

print(f"Node {leader} crashed")

leader_alive = False

time.sleep(5)

# -----------------------------------
# CLIENT TRANSACTION
# -----------------------------------

print("\n")
print("Leader Election Complete")
print(f"Leader is Node {leader}")

print("\nClient Sending Transaction...")

transaction = "TX001 : Pay Rs 100"

print(
    f"Leader received transaction: {transaction}"
)

time.sleep(2)

# -----------------------------------
# PAXOS PREPARE PHASE
# -----------------------------------

print("\n")
print("PAXOS PREPARE PHASE")
print("-------------------")

for node in nodes:

    if node != leader:

        print(
            f"Leader -> Node {node} : PREPARE"
        )

        print(
            f"Node {node} -> PROMISE"
        )

        time.sleep(0.5)

# -----------------------------------
# PAXOS ACCEPT PHASE
# -----------------------------------

print("\n")
print("PAXOS ACCEPT PHASE")
print("------------------")

accepted_count = 0

for node in nodes:

    if node != leader:

        print(
            f"Leader -> Node {node} : ACCEPT"
        )

        print(
            f"Node {node} -> ACCEPTED"
        )

        accepted_count += 1

        time.sleep(0.5)

# -----------------------------------
# CONSENSUS RESULT
# -----------------------------------

print("\n")
print("CONSENSUS RESULT")
print("----------------")

if accepted_count >= 2:

    print("Majority Reached")

    print("Transaction COMMITTED")

else:

    print("Consensus Failed")

time.sleep(5)