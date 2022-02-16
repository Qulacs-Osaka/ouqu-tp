import sys

from ouqu_tp.internal.ot_io import input_strings
from ouqu_tp.internal.simulate import simulate_do

input_strs = input_strings()
shots = int(sys.argv[1])
n_qubit = 0
(kekka, n_qubit) = simulate_do(input_strs, shots)
# input_listを直接ぶち込む
for aaaa in kekka:
    moziretu = "{:b}".format(aaaa)
    while len(moziretu) < n_qubit:
        moziretu = "0" + moziretu
    print(moziretu)
