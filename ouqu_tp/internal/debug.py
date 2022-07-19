import numpy as np
from qulacs import DensityMatrix, QuantumCircuit, QuantumState
from qulacs.gate import H
from qulacs.state import inner_product


def check_circuit(
    cirA: QuantumCircuit, cirB: QuantumCircuit, ok_rate: float = 0.999
) -> None:
    # ランダムなstateで6回試して、二つのcircuitが同じものかどうか確かめます。
    for i in range(6):
        stateA = QuantumState(cirA.get_qubit_count())
        if i > 0:
            stateA.set_Haar_random_state(i)
        else:
            H(0).update_quantum_state(stateA)
            H(1).update_quantum_state(stateA)

        stateB = stateA.copy()
        print(stateA)
        print(stateB)

        cirA.update_quantum_state(stateA)
        cirB.update_quantum_state(stateB)

        print(stateA)
        print(stateB)
        print("end")
        assert abs(inner_product(stateA, stateB)) > ok_rate
    return


def check_circuit_DM(
    cirA: QuantumCircuit, cirB: QuantumCircuit, ok_rate: float = 0.999
) -> None:
    # DensityMatrix で試します 純粋量子状態のinner_productの拡張になるはずだが、未証明
    stateA = DensityMatrix(cirA.get_qubit_count())
    stateA.set_Haar_random_state()
    stateB = stateA.copy()

    cirA.update_quantum_state(stateA)
    cirB.update_quantum_state(stateB)

    stateB.multiply_coef(-1)
    stateA.add_state(stateB)

    ABvec = stateA.get_matrix()
    gosa = 0
    for it in ABvec:
        for jt in it:
            gosa += jt * np.conj(jt)

    assert 1 - gosa / 2 > ok_rate * ok_rate

    return
