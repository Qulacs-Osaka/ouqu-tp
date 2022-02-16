import sys

from ouqu_tp.internal.ot_io import input_strings
from ouqu_tp.internal.sampleval import sampleval_noise_do

input_strs = input_strings()
shots = int(sys.argv[2])
p1 = float(sys.argv[3])
p2 = float(sys.argv[4])
pm = float(sys.argv[5])
pp = float(sys.argv[6])
print(sampleval_noise_do(input_strs, sys.argv[1], shots, p1, p2, pm, pp))
