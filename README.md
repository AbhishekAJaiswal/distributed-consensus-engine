Distributed Consensus Engine

Overview

This project implements a distributed consensus engine using Python, Docker, Paxos, and PBFT (Practical Byzantine Fault Tolerance). The objective is to simulate how distributed nodes coordinate to reach agreement while handling failures and malicious behavior.

The system consists of five nodes running as Docker containers. Each node participates in consensus protocols and communicates.

---

Features

* Leader Election
* Paxos Consensus Protocol
* PBFT Consensus Protocol
* RSA Digital Signatures
* Byzantine Adversary Simulation
* Chaos Testing (Node Failure and Recovery)
* Dockerized Multi-Node Deployment

---

Project Structure

```text
distributed-consensus-engine/
│
├── src/
│   ├── node.py
│   ├── client.py
│   ├── crypto_utils.py
│   └── adversary.py
│
├── tests/
│   └── chaos_test.sh
│
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── test_crypto.py
```

---

Technologies Used

* Python 3
* Flask
* Docker
* Docker Compose
* RSA Cryptography
* REST APIs

---

Installation

Clone the repository:

```bash
git clone <repository-url>
cd distributed-consensus-engine
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

Running the Cluster

Build Docker images:

```bash
docker compose build
```

Start the cluster:

```bash
docker compose up -d
```

Verify running containers:

```bash
docker ps
```

The cluster consists of:

* node1
* node2
* node3
* node4
* node5

---

Testing Digital Signatures

Run:

```bash
python test_crypto.py
```

Expected output:

```text
True
```

This confirms that RSA signature generation and verification are working correctly.

---

Leader Election

Trigger leader election:

```powershell
Invoke-RestMethod http://localhost:5001/elect
```

The system selects the highest active node ID as the leader.

---

Paxos Consensus

Paxos is implemented using the Prepare and Accept phases.

The leader sends:

* PREPARE requests
* ACCEPT requests

Consensus is achieved when a majority of nodes respond positively.

---

PBFT Consensus

Run the client:

```bash
python src/client.py
```

Enter a transaction ID:

```text
TX100
```

The transaction follows:

1. Pre-Prepare
2. Prepare
3. Commit

After receiving sufficient confirmations, the transaction is committed.

---

Byzantine Adversary Simulation

Run:

```bash
python src/adversary.py
```

This simulates a malicious node sending forged PBFT messages to evaluate fault tolerance.

---

Chaos Testing

Simulate node failure:

```bash
docker stop node3
```

Recover the node:

```bash
docker start node3
```

This demonstrates system resiliency and recovery under failures.

---

Results

The implemented system successfully demonstrates:

* Distributed leader election
* Paxos consensus
* PBFT consensus
* Digital signature verification
* Byzantine fault simulation
* Recovery from node failures

---

Author

Abhishek Anand Jaiswal

Distributed Systems Assignment
