from typing import List

from qulacs import DensityMatrix, QuantumState, observable

from ouqu_tp.internal.auto_noise import auto_evo_noise, auto_noise
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


def getval_noiseevo_do(
    input_strs: List[str],
    ferfile: str,
    shots: int,
    dt: float,
    OZ: float,
    OX: float,
    ORes: float,
    decay_rate_ph: float,
    decay_rate_amp: float,
    evodt: float,
) -> float:
    precircuit = QASM_to_qulacs(input_strs, remap_remove=True)
    testcircuit = auto_evo_noise(
        precircuit, dt, OZ, OX, ORes, decay_rate_ph, decay_rate_amp, evodt
    )
    # print(testcircuit)
    ans = 0.0
    obs = observable.create_observable_from_openfermion_file(ferfile)
    for _ in range(shots):
        out_state = QuantumState(testcircuit.get_qubit_count())
        testcircuit.update_quantum_state(out_state)
        ans += float(obs.get_expectation_value(out_state)) / shots
    return ans
