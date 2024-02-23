"""
This module contains the main benchmarking class `Benchmark`.
"""

import json
import itertools

from qiskit.converters import dag_to_circuit, circuit_to_dag

from .runner import Runner
from .inputs.default import gather_qasm_file_names


class Benchmark:
    """
    The main benchmarking class.
    A benchmark is built upon a list of input circuits, a list of transpilation stacks,
    and a list of metrics to record.
    """

    def __init__(self, inputs=None, passes=None, metrics=None, targets=None):
        self.inputs = inputs
        self.passes = passes
        self.metrics = metrics
        self.targets = targets

    @staticmethod
    def from_file(fname):
        """Build a Benchmark object from a json file"""
        with open(fname, "r") as fin:
            return Benchmark(**json.loads(fin.read()))

    def run(self, nprocesses=1):
        """
        Runs the full benchmark
        """
        # flattening the inputs
        all_inputs = []
        for dirname in self.inputs:
            all_inputs.extend(gather_qasm_file_names(dirname))
        iterator = itertools.product(self.passes.items(), self.targets.items())

        for tpass, target in iterator:
            runner = Runner(tpass, target, all_inputs)
            runner.run_benchmarks()
