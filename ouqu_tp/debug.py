from qulacs import QuantumCircuit, QuantumState
from qulacs.state import inner_product

def check_circuit(cirA,cirB):
    #ランダムなstateで6回試して、二つのcircuitが同じものかどうか確かめます。
    for i in range(6):
        stateA = QuantumState(cirA.get_qubit_count())
        stateA.set_Haar_random_state(i)
        stateB = stateA.copy()

        cirA.update_quantum_state(stateA)
        cirB.update_quantum_state(stateB)

        assert abs(inner_product(stateA, stateB)) > 0.9999