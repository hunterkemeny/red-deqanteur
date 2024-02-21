import statistics
from pytket.architecture import Architecture
from pytket.circuit import OpType, Node
from pytket.passes import *
from pytket.placement import NoiseAwarePlacement
from pytket.qasm import circuit_from_qasm_str
from pytket.qasm import circuit_to_qasm_str

from qiskit.circuit import QuantumCircuit

from .external import ExternalPassManager


class PytketPassManager(ExternalPassManager):
    """
    A pytket pass manager
    """

    def __init__(self, target, optimization_level: int):
        self.optimization_level = optimization_level
        self._errors = None
        super().__init__(target)

    def to_external_target(self, qiskit_target):
        averaged_node_gate_errors = {}
        averaged_edge_gate_errors = {}
        averaged_readout_errors = {}
        # averaged_readout_errors = {
        #     Node(x[0]): qiskit_target["measure"][x].error
        #     for x in qiskit_target["measure"]
        # }
        # for qarg in qiskit_target.qargs:
        #     ops = [
        #         x
        #         for x in qiskit_target.operation_names_for_qargs(qarg)
        #         if x not in {"if_else", "measure", "delay"}
        #     ]
        #     errors = [
        #         qiskit_target[op][qarg].error
        #         for op in ops
        #         if qiskit_target[op][qarg].error is not None
        #     ]
        #     if errors:
        #         avg = statistics.mean(errors)
        #     else:
        #         avg = 0  # or some other default value

        #     if len(qarg) == 1:
        #         averaged_node_gate_errors[Node(qarg[0])] = avg
        #     else:
        #         averaged_edge_gate_errors[tuple(Node(x) for x in qarg)] = avg
        self._errors = (
            averaged_node_gate_errors,
            averaged_edge_gate_errors,
            averaged_readout_errors,
        )
        return Architecture(qiskit_target.build_coupling_map().graph.edge_list())

    def to_external_circuit(self, qiskit_circuit: QuantumCircuit):
        return circuit_from_qasm_str(qiskit_circuit.qasm())

    def from_external_circuit(self, external_circuit) -> QuantumCircuit:
        """
        Converts an external circuit back to a qiskit circuit
        """
        print(external_circuit)
        return QuantumCircuit.from_qasm_str(circuit_to_qasm_str(external_circuit))

    def run_external_transpilation(self, external_circuit, external_target):
        """Run the pass manager on an external circuit."""
        transp_pass = self._build_tket_pass(self.optimization_level, external_target)
        transp_pass.apply(external_circuit)
        return external_circuit

    def _build_tket_pass(self, optimization_level: int, arch: Architecture):
        passlist = [DecomposeBoxes()]
        rebase_pass = auto_rebase_pass({OpType.X, OpType.SX, OpType.Rz, OpType.CZ})
        if optimization_level == 0:
            passlist.append(rebase_pass)
        elif optimization_level == 1:
            passlist.append(SynthesiseTket())
        elif optimization_level == 2:
            passlist.append(FullPeepholeOptimise())
        mid_measure = True
        (
            averaged_node_gate_errors,
            averaged_edge_gate_errors,
            averaged_readout_errors,
        ) = self._errors
        noise_aware_placement = NoiseAwarePlacement(
            arch,
            averaged_node_gate_errors,
            averaged_edge_gate_errors,
            averaged_readout_errors,
        )
        passlist.append(
            CXMappingPass(
                arch,
                noise_aware_placement,
                directed_cx=True,
                delay_measures=(not mid_measure),
            )
        )
        passlist.append(NaivePlacementPass(arch))
        if optimization_level == 1:
            passlist.append(SynthesiseTket())
        if optimization_level == 2:
            passlist.extend(
                [
                    KAKDecomposition(allow_swaps=False),
                    CliffordSimp(False),
                    SynthesiseTket(),
                ]
            )
        passlist.extend([rebase_pass, RemoveRedundancies()])
        passlist.append(SimplifyInitial(allow_classical=False, create_all_qubits=True))
        tket_pm = SequencePass(passlist)
        return tket_pm
