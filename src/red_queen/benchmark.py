"""
This module contains the main benchmarking class `Benchmark`.
"""

import json
import itertools
import logging

import pandas as pd

from .loader import load_object
from .runner import Runner
from .inputs.default import gather_qasm_file_names
from .utils import compute_metrics

_LOGGER = logging.getLogger("red_queen.benchmark")

_KEYS = ["circuit_name", "target"]


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

    def create_multi_index(self):
        """
        Creates a pandas MulitIndex object of shape (pass, metric) for all pairs passes/metrics
        """
        metrics = list(self.metrics.keys())
        passes = list(self.passes.keys())
        return pd.MultiIndex.from_tuples(
            [passes, metrics], names=["compiler", "metric"]
        )

    def run(self):
        """
        Runs the full benchmark
        """
        # flattening the inputs
        _LOGGER.info("Loading input circuits")
        all_inputs = []
        for dirname in self.inputs:
            all_inputs.extend(gather_qasm_file_names(dirname))
        _LOGGER.info("Loaded %d input circuits", len(all_inputs))

        _LOGGER.info("Loading metrics")
        metrics = {name: load_object(value) for name, value in self.metrics.items()}
        _LOGGER.info("Loaded %d metrics", len(metrics))

        multi_index = self.create_multi_index()
        full_data = []
        for target in self.targets.items():
            for tpass in self.passes.items():
                runner = Runner(tpass, target, all_inputs)
                runner.run_benchmarks()

                full_data.extend(
                    compute_metrics(dictionary, metrics)
                    for dictionary in runner.results
                )
        full_df = pd.DataFrame(full_data)
        return full_df
