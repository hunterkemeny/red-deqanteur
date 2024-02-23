import os
from qiskit.circuit import QuantumCircuit


def load_qasm(fname):
    return QuantumCircuit.from_qasm_file(fname)


def gather_qasm_file_names(directory):
    _, _, files = next(os.walk(directory))
    for fname in files:
        if not fname.endswith(".qasm"):
            continue
        yield os.path.join(directory, fname)


# @gen_to_list
def load_qasm_circuits(directory, max_n_qubits):
    """
    Load all qasm circuits from a given target directory
    """
    _, _, files = next(os.walk(directory))
    for fname in files:
        if not fname.endswith(".qasm"):
            continue
        circuit = QuantumCircuit.from_qasm_file(os.path.join(directory, fname))
        if circuit.num_qubits <= max_n_qubits:
            yield circuit
