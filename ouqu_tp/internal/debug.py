from qulacs import QuantumCircuit, QuantumState
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
