import sys
from benchmark import Benchmark


benchmark = Benchmark.from_file(sys.argv[1])
benchmark.run()
