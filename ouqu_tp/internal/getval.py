from typing import List

from qulacs import DensityMatrix, QuantumState, observable

from ouqu_tp.internal.auto_noise import auto_noise
from ouqu_tp.internal.QASMtoqulacs import QASM_to_qulacs


def getval_do(input_strs: List[str], ferfile: str) -> float:
    testcircuit = QASM_to_qulacs(input_strs, remap_remove=True)

    out_state = QuantumState(testcircuit.get_qubit_count())
    testcircuit.update_quantum_state(out_state)

    obs = observable.create_observable_from_openfermion_file(ferfile)
    return float(obs.get_expectation_value(out_state))
    # qulacsの型アノテーションないので、怒りのキャスト


def getval_noise_do(
    input_strs: List[str], ferfile: str, p1: float, p2: float, pm: float, pp: float
) -> float:

    precircuit = QASM_to_qulacs(input_strs, remap_remove=True)
    testcircuit = auto_noise(precircuit, p1, p2, pm, pp)

    out_state = DensityMatrix(testcircuit.get_qubit_count())
    testcircuit.update_quantum_state(out_state)

    obs = observable.create_observable_from_openfermion_file(ferfile)
    return float(obs.get_expectation_value(out_state))
    # qulacsの型アノテーションないので、怒りのキャスト
