from typing import List, Tuple

from qulacs import NoiseSimulator, QuantumCircuit, QuantumState

from ouqu_tp.internal.auto_noise import auto_noise
from ouqu_tp.internal.ot_io import str_to_gate


def simulate_do(input_strs: List[str], shots: int) -> Tuple[List[int], int]:
    print(input_strs)
    (n_qubit, input_list) = str_to_gate(input_strs, "notput", True)

    testcircuit = QuantumCircuit(n_qubit)
    for it in input_list:
        testcircuit.add_gate(it)

    out_state = QuantumState(n_qubit)
    testcircuit.update_quantum_state(out_state)
    print(out_state)
    kekka = out_state.sampling(shots)
    return (kekka, n_qubit)


def simulate_noise_do(
    input_strs: List[str], shots: int, p1: float, p2: float, pm: float, pp: float
) -> Tuple[List[int], int]:
    (n_qubit, input_list) = str_to_gate(input_strs, "notput", True)

    testcircuit = auto_noise(input_list, n_qubit, p1, p2, pm, pp)

    out_state = QuantumState(n_qubit)
    nsim = NoiseSimulator(testcircuit, out_state)

    kekka = nsim.execute(shots)
    return (kekka, n_qubit)
