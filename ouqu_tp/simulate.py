from typing import List, Tuple

from qulacs import QuantumCircuit, QuantumState

from ouqu_tp.ot_io import str_to_gate


def simulate_do(input_strs: List[str], shots: int) -> Tuple[List[int], int]:
    (n_qubit, input_list) = str_to_gate(input_strs, "notput")
    testcircuit = QuantumCircuit(n_qubit)
    for it in input_list:
        testcircuit.add_gate(it)
    out_state = QuantumState(n_qubit)
    testcircuit.update_quantum_state(out_state)
    kekka = out_state.sampling(shots)
    return (kekka, n_qubit)
