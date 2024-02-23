from qiskit.converters import circuit_to_dag, dag_to_circuit
from qiskit.transpiler.passes import BasisTranslator
from qiskit.circuit.equivalence_library import SessionEquivalenceLibrary as sel


def entangling_count(circuit):
    """
    Returns the CNOT equivalent count of the circuit
    """
    dag = circuit_to_dag(circuit)
    dag = BasisTranslator(sel, target_basis=["cx", "u3"]).run(dag)
    return dag.count_ops()["cx"]


def entangling_depth(circuit):
    """
    Returns the CNOT equivalent count of the circuit
    """
    dag = circuit_to_dag(circuit)
    dag = BasisTranslator(sel, target_basis=["cx", "u3"]).run(dag)
    circuit = dag_to_circuit(dag)
    return circuit.depth(lambda q: q.operation.name == "cx")
