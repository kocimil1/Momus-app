# Installation Instructions

Follow these steps to set up your environment:

## Prerequisites

Ensure you have the following installed on your system:
- Python 3
- pip (Python package installer)
- Node.js
- npm (Node Package Manager)

You can install Python 3, pip, Node.js, and npm on Ubuntu using the following command:

```bash
sudo apt-get update
sudo apt-get install python3 python3-pip nodejs npm

pip install -I qiskit[visualization] qiskit-ibm-runtime qiskit-nature[pyscf]
pip install py3Dmol flask

python3 run.py