from cmath import pi

from qulacs import QuantumCircuit

from ouqu_tp.internal.debug import check_circuit
from ouqu_tp.internal.tran import pulse_to_circuit
from ouqu_tp.internal.trancepile import trance_pulse_do


def test_kairo_pulse() -> None:
    # staq->ouqu と、　qulacsのゲートが、同じかどうか確かめます
    taiou = [0, 3, 6, 2, 1]
    circuit = QuantumCircuit(7)

    kak = 3.14159265 / 20
    circuit.add_U3_gate(taiou[0], kak * 8, kak * 7, kak * 4)
    circuit.add_U2_gate(taiou[1], -kak * 3, kak * 6)
    circuit.add_RY_gate(taiou[4], kak * 7)
    circuit.add_U1_gate(taiou[2], kak * 3)
    circuit.add_CNOT_gate(taiou[0], taiou[2])

    circuit.add_X_gate(taiou[2])
    circuit.add_CNOT_gate(taiou[4], taiou[3])
    circuit.add_Y_gate(taiou[1])

    circuit.add_RX_gate(taiou[2], kak * 4)
    circuit.add_Z_gate(taiou[4])
    circuit.add_H_gate(taiou[0])

    circuit.add_S_gate(taiou[1])
    circuit.add_CNOT_gate(taiou[4], taiou[2])

    circuit.add_CZ_gate(taiou[1], taiou[3])

    circuit.add_Sdag_gate(taiou[4])
    circuit.add_T_gate(taiou[0])
    circuit.add_Tdag_gate(taiou[1])

    input_strs = [
        "qreg q[7];",
        "U(1.256637,1.09955742,0.6283185) q[0];",
        "U(1.5707963267949,-0.47123889,0.94247779) q[3];",
        "U(-1.09955742,0,0) q[1];",
        "U(0,0,0.47123889) q[6];",
        "CX q[1],q[6];",
        "CX q[0],q[1];",
        "CX q[1],q[6];",
        "CX q[0],q[1];",
        "U(3.14159265358979,0,3.14159265358979) q[6];",
        "CX q[1],q[2];",
        "U(3.14159265358979,1.5707963267949,1.5707963267949) q[3];",
        "U(-0.6283185,-1.5707963267949,1.5707963267949) q[6];",
        "U(0,0,3.14159265358979) q[1];",
        "U(1.5707963267949,0,3.14159265358979) q[0];",
        "U(0,0,1.5707963267949) q[3];",
        "CX q[1],q[6];",
        "U(1.5707963267949,0,3.14159265358979) q[2];",
        "CX q[3],q[2];",
        "U(1.5707963267949,0,3.14159265358979) q[2];",
        "U(0,0,-0.785398163397448) q[3];",
        "U(0,0,-1.5707963267949) q[1];",
        "U(0,0,0.785398163397448) q[0];",
    ]
    Cnet_list = [
        "test",
        "7",
        "4",
        "1,6",
        "0,1",
        "1,2",
        "3,2",
    ]
    pulse_array = trance_pulse_do(input_strs, Cnet_list, pi / 20, 1, 1, 0.25, 5)
    n_qubit = 7
    Res_list = [(1, 6), (0, 1), (1, 2), (3, 2)]
    testcircuit = pulse_to_circuit(n_qubit, pulse_array, Res_list)
    # print(testcircuit)
    # パルスが整数の長さしか取れないので、　誤差が生じるから閾値が0.9
    check_circuit(circuit, testcircuit, 0.9)
