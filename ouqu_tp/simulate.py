import sys

from ot_io import input_strings, str_to_gate
from qulacs import QuantumCircuit, QuantumState

def simulate_do(input_strs ,shots:int):
    (n_qubit, input_list) = str_to_gate(input_strs, "notput")
    testcircuit = QuantumCircuit(n_qubit)
    for it in input_list:
        testcircuit.add_gate(it)
    out_state = QuantumState(n_qubit)
    testcircuit.update_quantum_state(out_state)
    kekka = out_state.sampling(shots)
    return kekka
    

input_strs = input_strings()
shots = int(sys.argv[1])
kekka=simulate_do(input_strs,shots)
# input_listを直接ぶち込む
for aaaa in kekka:
    moziretu = "{:b}".format(aaaa)
    while len(moziretu) < n_qubit:
        moziretu = "0" + moziretu
    print(moziretu)
    
