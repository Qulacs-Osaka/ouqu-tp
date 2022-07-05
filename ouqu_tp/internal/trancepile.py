from typing import List

import numpy as np
import numpy.typing as npt

from ouqu_tp.internal.make_Cnet import get_connect
from ouqu_tp.internal.QASMtoqulacs import QASM_to_qulacs, qulacs_to_QASM
from ouqu_tp.internal.tran import CNOT_to_CRes, tran_ouqu_multi, tran_to_pulse


def trance_do(input_strs: List[str]) -> List[str]:
    mtocircuit = QASM_to_qulacs(input_strs, remap_remove=False)
    trancircuit = tran_ouqu_multi(mtocircuit)
    return qulacs_to_QASM(trancircuit)


def trance_res_do(input_strs: List[str]) -> List[str]:
    mtocircuit = QASM_to_qulacs(input_strs, remap_remove=False)
    mtocircuit = CNOT_to_CRes(mtocircuit)
    trancircuit = tran_ouqu_multi(mtocircuit)
    return qulacs_to_QASM(trancircuit)


def trance_pulse_do(
    input_strs: List[str],
    Cnet_list: List[str],
    dt: float,
    OZ: float,
    OX: float,
    ORes: float,
    mergen: int = 0,
) -> npt.NDArray[np.float64]:
    mtocircuit = QASM_to_qulacs(input_strs, remap_remove=False)
    Res_list = get_connect(Cnet_list)
    result_array = tran_to_pulse(mtocircuit, Res_list, dt, OZ, OX, ORes, mergen)
    return result_array
