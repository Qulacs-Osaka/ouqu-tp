from typing import List, Tuple

from qulacs import (
    NoiseSimulator,
    QuantumCircuit,
    QuantumGateBase,
    QuantumState,
)
from qulacs.gate import DepolarizingNoise, TwoQubitDepolarizingNoise

from ouqu_tp.ot_io import str_to_gate


def auto_noize(
    gate_list: List[QuantumGateBase],
    n_qubit: int,
    p1: float,
    p2: float,
    pm: float,
    pp: float,
) -> QuantumCircuit:
    testcircuit = QuantumCircuit(n_qubit)
    for i in range(n_qubit):
        testcircuit.add_gate(DepolarizingNoise(i, pp))
    for ingate in gate_list:
        testcircuit.add_gate(ingate)

        gate_index_list = (
            ingate.get_control_index_list() + ingate.get_target_index_list()
        )
        if len(gate_index_list) == 1:
            testcircuit.add_gate(DepolarizingNoise(gate_index_list[0], p1))
        if len(gate_index_list) == 2:
            testcircuit.add_gate(
                TwoQubitDepolarizingNoise(gate_index_list[0], gate_index_list[1], p2)
            )

        if len(gate_index_list) > 2:
            # 本来ありえません　3ビット以上のやつは
            raise RuntimeError("3ビット以上のやつを与えないでください もしくは何かバグがあるので、連絡して下さい")

    for i in range(n_qubit):
        testcircuit.add_gate(DepolarizingNoise(i, pm))
    return testcircuit


def noisesim_do(
    input_strs: List[str], shots: int, p1: float, p2: float, pm: float, pp: float
) -> Tuple[List[int], int]:
    (n_qubit, input_list) = str_to_gate(input_strs, "notput")
    testcircuit = auto_noize(input_list, n_qubit, p1, p2, pm, pp)

    out_state = QuantumState(n_qubit)
    nsim = NoiseSimulator(testcircuit, out_state)
    kekka = nsim.execute(shots)
    return (kekka, n_qubit)
