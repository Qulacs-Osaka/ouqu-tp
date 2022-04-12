from math import sqrt

import numpy as np
from qulacs import QuantumCircuit
from qulacs.gate import DenseMatrix

from ouqu_tp.internal.debug import check_circuit
from ouqu_tp.internal.QASMtoqulacs import QASM_to_qulacs, qulacs_to_QASM


def test_cirQASMcir() -> None:
    # circuit -> QASM -> circuit して、回路が同じかどうか確かめます
    circuit = QuantumCircuit(5)
    circuit.add_U3_gate(2, 1.2, 2.1, 0.9)
    circuit.add_U2_gate(1, -0.5, 1.2)
    circuit.add_RY_gate(4, -1.4)
    circuit.add_U1_gate(2, 0.4)
    circuit.add_CNOT_gate(0, 2)
    circuit.add_X_gate(2)
    circuit.add_CNOT_gate(4, 3)
    circuit.add_Y_gate(1)
    circuit.add_RX_gate(2, -1.2)
    circuit.add_Z_gate(4)
    gate_mat = np.array(
        [[1, 0, -1.0j, 0], [0, 1, 0, 1.0j], [-1.0j, 0, 1, 0], [0, 1.0j, 0, 1]]
    )
    dense_gate = DenseMatrix([0, 1], gate_mat / sqrt(2))
    dense_gate.add_control_qubit(2, 1)
    circuit.add_gate(dense_gate)
    circuit.add_H_gate(0)
    circuit.add_S_gate(1)
    circuit.add_CNOT_gate(4, 2)
    circuit.add_CZ_gate(1, 3)
    circuit.add_Sdag_gate(4)
    circuit.add_T_gate(0)
    circuit.add_Tdag_gate(1)

    QASM_str = qulacs_to_QASM(circuit)

    rev_cir = QASM_to_qulacs(QASM_str)

    # print(testcircuit)
    check_circuit(circuit, rev_cir)
