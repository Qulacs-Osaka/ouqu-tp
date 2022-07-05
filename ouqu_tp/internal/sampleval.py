from typing import List

from qulacs import observable

from ouqu_tp.internal.auto_noise import auto_evo_noise, auto_noise
from ouqu_tp.internal.QASMtoqulacs import QASM_to_qulacs
from ouqu_tp.internal.shot_obs import (
    get_measurement,
    get_noise_meseurment,
    get_noiseevo_meseurment,
)


def sampleval_do(input_strs: List[str], ferfile: str, shots: int) -> float:
    testcircuit = QASM_to_qulacs(input_strs, remap_remove=True)

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
    precircuit = QASM_to_qulacs(input_strs, remap_remove=True)
    testcircuit = auto_noise(precircuit, p1, p2, pm, pp)

    obs = observable.create_observable_from_openfermion_file(ferfile)
    return get_noise_meseurment(testcircuit, obs, shots)


def sampleval_noiseevo_do(
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

    obs = observable.create_observable_from_openfermion_file(ferfile)
    return get_noiseevo_meseurment(testcircuit, obs, shots)
