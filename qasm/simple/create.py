from qiskit.circuit.library import CDKMRippleCarryAdder
from qiskit.qasm2 import dump

for i in range(5, 20):
    adder = CDKMRippleCarryAdder(i).decompose().decompose()
    dump(adder, f"./adder_{i}.qasm")
