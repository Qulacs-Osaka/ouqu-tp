from typing import List, Tuple

from qulacs import NoiseSimulator, QuantumState

from ouqu_tp.internal.auto_noise import auto_evo_noise, auto_noise
from ouqu_tp.internal.QASMtoqulacs import QASM_to_qulacs


def simulate_do(input_strs: List[str], shots: int) -> Tuple[List[int], int]:
    testcircuit = QASM_to_qulacs(input_strs, remap_remove=True)
    n_qubit = testcircuit.get_qubit_count()

    out_state = QuantumState(n_qubit)
    testcircuit.update_quantum_state(out_state)
    kekka = out_state.sampling(shots)
    return (kekka, n_qubit)


def simulate_noise_do(
    input_strs: List[str], shots: int, p1: float, p2: float, pm: float, pp: float
) -> Tuple[List[int], int]:
    precircuit = QASM_to_qulacs(input_strs, remap_remove=True)
    testcircuit = auto_noise(precircuit, p1, p2, pm, pp)
    n_qubit = testcircuit.get_qubit_count()

    out_state = QuantumState(n_qubit)
    nsim = NoiseSimulator(testcircuit, out_state)

    kekka = nsim.execute(shots)
    return (kekka, n_qubit)


def simulate_noiseevo_do(
    input_strs: List[str],
    shots: int,
    dt: float,
    OZ: float,
    OX: float,
    ORes: float,
    decay_rate_ph: float,
    decay_rate_amp: float,
    evodt: float,
) -> Tuple[List[int], int]:
    precircuit = QASM_to_qulacs(input_strs, remap_remove=True)
    testcircuit = auto_evo_noise(
        precircuit, dt, OZ, OX, ORes, decay_rate_ph, decay_rate_amp, evodt
    )
    n_qubit = testcircuit.get_qubit_count()

    out_state = QuantumState(n_qubit)
    kekka = []
    for _ in range(shots):
        out_state.set_zero_state()
        testcircuit.update_quantum_state(out_state)
        kekka.append(out_state.sampling(1)[0])
    return (kekka, n_qubit)
