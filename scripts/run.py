import sys
from red_queen.benchmark import Benchmark


benchmark = Benchmark.from_file(sys.argv[1])
benchmark.run()
