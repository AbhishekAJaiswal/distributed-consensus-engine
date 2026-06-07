print("PBFT MODE")

print("\nPRE-PREPARE PHASE")
print("-----------------")

print("Primary Node -> TX001 : Pay Rs 100")

print("\nPREPARE PHASE")
print("-------------")

for i in range(1, 6):
    print(f"Node {i} -> PREPARE")

print("\nBYZANTINE ATTACK")
print("----------------")

print("Adversary Node 99 sent conflicting transaction")
print("Signature Verification Failed")
print("Ignoring Malicious Node")

print("\nCOMMIT PHASE")
print("------------")

for i in range(1, 6):
    print(f"Node {i} -> COMMIT")

print("\nPBFT RESULT")
print("-----------")
print("Transaction COMMITTED")