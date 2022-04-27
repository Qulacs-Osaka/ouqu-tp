from typing import List

from qulacs import QuantumCircuit, QuantumGateBase
from qulacs.gate import DepolarizingNoise, TwoQubitDepolarizingNoise


def auto_noise(
    inputcircuit: QuantumCircuit,
    p1: float,
    p2: float,
    pm: float,
    pp: float,
) -> QuantumCircuit:
    n_qubit = inputcircuit.get_qubit_count()
    testcircuit = QuantumCircuit(n_qubit)
    for i in range(n_qubit):
        testcircuit.add_gate(DepolarizingNoise(i, pp))
    gate_num = inputcircuit.get_gate_count()
    for i in range(gate_num):
        ingate=inputcircuit.get_gate(i)
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
