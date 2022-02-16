import sys

from ouqu_tp.internal.ot_io import input_strings
from ouqu_tp.internal.sampleval import sampleval_do

input_strs = input_strings()
shots = int(sys.argv[2])
print(sampleval_do(input_strs, sys.argv[1], shots))
