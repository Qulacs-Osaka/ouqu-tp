from qulacs import QuantumCircuit, QuantumState

from ouqu_tp.internal.auto_noise import auto_evo_noise
from ouqu_tp.internal.debug import check_circuit, check_circuit_DM


def test_kairo_noiseevo() -> None:
    # state auto_noiseでnoise=0 の場合、パルス整数誤差程度であることを証明
    # noiseevoがDMに対応しないことが判明
    circuit = QuantumCircuit(5)
    kak = 3.14159265 / 20

    circuit.add_U3_gate(0, kak * 8, kak * 7, kak * 4)
    circuit.add_U2_gate(1, -kak * 3, kak * 6)
    circuit.add_CNOT_gate(3, 2)
    circuit.add_RY_gate(4, kak * 7)
    circuit.add_U1_gate(2, kak * 3)
    circuit.add_CNOT_gate(0, 2)
    circuit.add_X_gate(2)
    circuit.add_CNOT_gate(4, 3)
    circuit.add_Y_gate(1)
    circuit.add_RX_gate(2, kak * 4)
    circuit.add_Z_gate(4)
    circuit.add_H_gate(0)
    circuit.add_S_gate(1)
    circuit.add_CNOT_gate(4, 2)
    circuit.add_CNOT_gate(3, 2)
    circuit.add_Sdag_gate(4)
    circuit.add_T_gate(0)
    circuit.add_Sdag_gate(1)
    circuit.add_CNOT_gate(2, 0)

    testcircuit = auto_evo_noise(circuit, kak, 0.5, 0.5, 0.25, 0.000001, 0.000001, 0.1)
    check_circuit(circuit, testcircuit, 0.99)
    # check_circuit_DM(circuit, testcircuit, 0.99)
