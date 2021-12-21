import sys

from ot_io import input_strings, str_to_gate
from qulacs import QuantumCircuit, QuantumState, observable

def getval_do(input_strs ,ferfile :str):
    (n_qubit, input_list) = str_to_gate(input_strs, "notput")
    # input_listを直接ぶち込む
    testcircuit = QuantumCircuit(n_qubit)
    for it in input_list:
        testcircuit.add_gate(it)
    out_state = QuantumState(n_qubit)
    testcircuit.update_quantum_state(out_state)

    obs = observable.create_observable_from_openfermion_file(ferfile)

    return obs.get_expectation_value(out_state)


input_strs = input_strings()
print(getval_do(input_strs,sys.argv[1]))



