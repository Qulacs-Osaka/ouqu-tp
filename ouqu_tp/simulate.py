from ot_io import input_strings, str_to_gate
from qulacs import QuantumCircuit, QuantumState

input_strs = input_strings()
(n_qubit, input_list) = str_to_gate(input_strs, "notput")

# input_listを直接ぶち込む
testcircuit = QuantumCircuit(n_qubit)
for it in input_list:
    testcircuit.add_gate(it)
out_state = QuantumState(n_qubit)
testcircuit.update_quantum_state(out_state)
shots = 100
kekka = out_state.sampling(shots)
# print(kekka)
for aaaa in kekka:
    moziretu = "{:b}".format(aaaa)
    while len(moziretu) < n_qubit:
        moziretu = "0" + moziretu
    print(moziretu)
