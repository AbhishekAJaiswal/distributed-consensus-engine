import time

# -----------------------------------
# LEADER ELECTION
# -----------------------------------

nodes = [1, 2, 3, 4, 5]

print("Initial Election\n")

for node in nodes[:-1]:
    print(f"Node {node} is Follower")

print("Node 5 is Leader")

time.sleep(2)

# -----------------------------------
# LEADER FAILURE RECOVERY
# -----------------------------------

print("\n")
print("Leader Crash")
print("----------------")

print("Node 5 crashed")

nodes.remove(5)

new_leader = max(nodes)

print(f"Node {new_leader} elected as new Leader")

time.sleep(2)

# -----------------------------------
# CLIENT TRANSACTION
# -----------------------------------

print("\n")
print("Leader Election Complete")
print(f"Leader is Node {new_leader}")

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

    if node != new_leader:

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

    if node != new_leader:

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