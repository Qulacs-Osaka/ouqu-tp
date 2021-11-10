from qulacs import QuantumCircuit, QuantumState
from qulacs.state import inner_product


def simulate_circuit(cir: QuantumCircuit) -> QuantumState:

    n_qubit=cir.get_qubit_count()
    sta=QuantumState(n_qubit)
    cir.update_quantum_state(sta)
    return sta