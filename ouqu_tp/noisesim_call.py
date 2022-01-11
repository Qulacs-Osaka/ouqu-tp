import sys

from ouqu_tp.noisesim import noisesim_do
from ouqu_tp.ot_io import input_strings

input_strs = input_strings()
shots = int(sys.argv[1])
n_qubit = 0

p1 = float(sys.argv[2])
p2 = float(sys.argv[3])
pm = float(sys.argv[4])
pp = float(sys.argv[5])
(kekka, n_qubit) = noisesim_do(input_strs, shots, p1, p2, pm, pp)
# input_listを直接ぶち込む
for aaaa in kekka:
    moziretu = "{:b}".format(aaaa)
    while len(moziretu) < n_qubit:
        moziretu = "0" + moziretu
    print(moziretu)
