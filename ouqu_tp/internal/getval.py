from typing import List

from qulacs import DensityMatrix, QuantumCircuit, QuantumState, observable

from ouqu_tp.internal.auto_noise import auto_noise
from ouqu_tp.internal.ot_io import str_to_gate


def getval_do(input_strs: List[str], ferfile: str) -> float:
    (n_qubit, input_list) = str_to_gate(input_strs, "notput", True)

    testcircuit = QuantumCircuit(n_qubit)
    for it in input_list:
        testcircuit.add_gate(it)

    out_state = QuantumState(n_qubit)
    testcircuit.update_quantum_state(out_state)

    obs = observable.create_observable_from_openfermion_file(ferfile)
    return float(obs.get_expectation_value(out_state))
    # qulacsの型アノテーションないので、怒りのキャスト


def getval_noise_do(
    input_strs: List[str], ferfile: str, p1: float, p2: float, pm: float, pp: float
) -> float:
    (n_qubit, input_list) = str_to_gate(input_strs, "notput", True)

    testcircuit = auto_noise(input_list, n_qubit, p1, p2, pm, pp)

    out_state = DensityMatrix(n_qubit)
    testcircuit.update_quantum_state(out_state)

    obs = observable.create_observable_from_openfermion_file(ferfile)
    return float(obs.get_expectation_value(out_state))
    # qulacsの型アノテーションないので、怒りのキャスト
