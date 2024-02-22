"""
This module contains the main benchmarking class `Benchmark`.
"""

import json
import itertools
import multiprocessing

from qiskit.converters import dag_to_circuit, circuit_to_dag

from loader import load_object
from utils import rebuild_dict
from runner import Runner

class Benchmark:
    """
    The main benchmarking class.
    A benchmark is built upon a list of input circuits, a list of transpilation stacks,
    and a list of metrics to record.
    """

    def __init__(self, optimization_levels=None, version=None, compiler=None, targets=None, num_runs=None):
        self.optimization_levels = optimization_levels
        self.version = version
        self.compiler = compiler
        self.targets = targets
        self.num_runs = num_runs

    @staticmethod
    def from_file(fname):
        """Build a Benchmark object from a json file"""
        with open(fname, "r") as fin:
            return Benchmark(**json.loads(fin.read()))

    def run(self):
        """
        Runs the full benchmark
        """

        optimization_levels = self.optimization_levels["optimization_levels"]['args']

        version = self.version["version"]['args'][0]
        compiler = self.compiler["compiler"]['args'][0]
        #expand to more targets later
        target = self.targets["ibm_washington"]['args'][0]
        num_runs = self.num_runs["num_runs"]['args'][0]

        for opt_level in optimization_levels:
            # here we want to run from red-queen
            runner = Runner(
                {
                    "compiler": compiler,
                    "version": version,
                    "optimization_level": opt_level,
                },
                str(target),  #backend
                int(num_runs), #num runs
            )
            runner.run_benchmarks()
            