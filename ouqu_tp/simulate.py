from qulacs import QuantumCircuit, QuantumState
from qulacs.state import inner_product


from ot_io import input_strings, output_gates_QASMfuu, str_to_gate
from tran import tran_ouqu_multi


input_strs = input_strings()
(n_qubit, input_list) = str_to_gate(input_strs)

#input_listを直接ぶち込む
testcircuit = QuantumCircuit(n_qubit)
for it in input_list:
    testcircuit.add_gate(it)
out_state=QuantumState(n_qubit)
testcircuit.update_quantum_state(out_state)
shots=100
kekka = out_state.sampling(shots)
#print(kekka)
for aaaa in kekka:
    moziretu='{:b}'.format(aaaa)
    while len(moziretu)<n_qubit:
        moziretu="0"+moziretu
    print(moziretu)
