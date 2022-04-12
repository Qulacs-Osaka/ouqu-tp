from math import pi, sqrt

import numpy as np
from qulacs import QuantumCircuit, QuantumState
from qulacs.gate import DenseMatrix
from qulacs.state import inner_product

cir = QuantumCircuit(2)
print(sqrt(2))
gate_mat = np.array(
    [[1, 0, -1.0j, 0], [0, 1, 0, 1.0j], [-1.0j, 0, 1, 0], [0, 1.0j, 0, 1]]
)
dense_gate = DenseMatrix([0, 1], gate_mat / sqrt(2))
print(dense_gate)
cir.add_RX_gate(1, pi / 2)
cir.add_gate(dense_gate)

cir.add_RZ_gate(0, pi / 2)

cir.add_CNOT_gate(0, 1)

state = QuantumState(2)

for i in range(4):
    state.set_Haar_random_state()
    aaa = [0, 0, 0, 0]
    aaa[i] = 1
    state.load(aaa)
    stateA = state.copy()
    cir.update_quantum_state(state)
    print(state)
    print(inner_product(state, stateA))
    #
