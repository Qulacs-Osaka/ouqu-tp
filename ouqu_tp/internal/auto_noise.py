from typing import List

from qulacs import QuantumCircuit, QuantumGateBase
from qulacs.gate import DepolarizingNoise, TwoQubitDepolarizingNoise


def auto_noise(
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
