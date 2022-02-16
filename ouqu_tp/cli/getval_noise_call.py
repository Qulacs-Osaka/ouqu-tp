import sys

from ouqu_tp.internal.getval import getval_noise_do
from ouqu_tp.internal.ot_io import input_strings

input_strs = input_strings()
p1 = float(sys.argv[2])
p2 = float(sys.argv[3])
pm = float(sys.argv[4])
pp = float(sys.argv[5])
print(getval_noise_do(input_strs, sys.argv[1], p1, p2, pm, pp))
