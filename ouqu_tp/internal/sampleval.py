from typing import List

from qulacs import QuantumCircuit, observable

from ouqu_tp.internal.auto_noise import auto_noise
from ouqu_tp.internal.ot_io import str_to_gate
from ouqu_tp.internal.shot_obs import get_measurement, get_noise_meseurment


def sampleval_do(input_strs: List[str], ferfile: str, shots: int) -> float:
    (n_qubit, input_list) = str_to_gate(input_strs, "notput")

    testcircuit = QuantumCircuit(n_qubit)
    for it in input_list:
        testcircuit.add_gate(it)

    obs = observable.create_observable_from_openfermion_file(ferfile)

    return get_measurement(testcircuit, obs, shots)


def sampleval_noise_do(
    input_strs: List[str],
    ferfile: str,
    shots: int,
    p1: float,
    p2: float,
    pm: float,
    pp: float,
) -> float:
    (n_qubit, input_list) = str_to_gate(input_strs, "notput")

    testcircuit = auto_noise(input_list, n_qubit, p1, p2, pm, pp)

    obs = observable.create_observable_from_openfermion_file(ferfile)

    return get_noise_meseurment(testcircuit, obs, shots)
