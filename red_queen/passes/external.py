import abc
from qiskit.transpiler import PassManager, Target
from qiskit.circuit import QuantumCircuit


class ExternalPassManager(PassManager, abc.ABC):
    """Base class for external pass managers."""

    def __init__(self, target=None):
        super().__init__(self)
        self.external_target = self.to_external_target(target)

    @abc.abstractmethod
    def to_external_target(self, qiskit_target: Target):
        """
        Converts a qiskit target to an external target.
        """

    @abc.abstractmethod
    def to_external_circuit(self, qiskit_circuit: QuantumCircuit):
        """
        Converts a qiskit circuit to an external circuit.
        """

    @abc.abstractmethod
    def from_external_circuit(self, external_circuit) -> QuantumCircuit:
        """
        Converts an external circuit back to a qiskit circuit
        """

    @abc.abstractmethod
    def run_external_transpilation(self, external_circuit, external_target):
        """Run the pass manager on an external circuit."""

    def run(self, circuit):
        """Run the pass manager on a circuit."""
        external_circuit = self.to_external_circuit(circuit)
        external_circuit = self.run_external_transpilation(
            external_circuit, self.external_target
        )
        return self.from_external_circuit(external_circuit)
