import multiprocessing
import time
import logging


from memory_profiler import memory_usage

from .loader import load_object
from .inputs.default import load_qasm

_LOGGER = logging.getLogger("red_queen.runner")


class Runner:
    def __init__(self, transpiler_pass: dict, target: dict, qasm_files: list):
        self.transpiled_key, self.transpiler_pass = transpiler_pass
        self.target_key, self.target = target
        self.qasm_files = qasm_files
        self.results = []

    def run_benchmarks(self):
        """
        Runs the benchmark
        """
        _LOGGER.log(logging.INFO, "Running benchmarks...")
        with multiprocessing.Pool(processes=1) as pool:
            for result in pool.map(self.run_on_file, self.qasm_files):
                print(result)
        _LOGGER.log(logging.INFO, "Computing metrics...")
        # TODO: compute metrics on the results and return a piece of DataFrame ?
        return results

    def run_on_file(self, qasm_file):

        target = load_object(self.target)
        circuit = load_qasm(qasm_file)
        start_mem = memory_usage(max_usage=True)
        start_time = time.perf_counter()
        circuit = load_object(self.transpiler_pass, target=target).run(circuit)
        end_mem = memory_usage(max_usage=True)
        memory = end_mem - start_mem
        transp_time = time.perf_counter() - start_time
        return {"circuit": circuit, "memory": memory, "time": transp_time}
