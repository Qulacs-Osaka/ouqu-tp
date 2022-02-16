import sys

from ouqu_tp.internal.getval import getval_do
from ouqu_tp.internal.ot_io import input_strings

input_strs = input_strings()
print(getval_do(input_strs, sys.argv[1]))
