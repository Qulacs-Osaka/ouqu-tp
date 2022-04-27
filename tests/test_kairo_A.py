from qulacs import QuantumCircuit

from ouqu_tp.internal.debug import check_circuit
from ouqu_tp.internal.ot_io import str_to_gate
from ouqu_tp.internal.tran import tran_ouqu_multi


def test_kairo_A() -> None:
    # staq->ouqu と、　qulacsのゲートが、同じかどうか確かめます
    taiou = [0, 3, 6, 2, 1]
    circuit = QuantumCircuit(7)
    circuit.add_U3_gate(taiou[0], 1.2, 2.1, 0.9)
    circuit.add_U2_gate(taiou[1], -0.5, 1.2)
    circuit.add_RY_gate(taiou[4], -1.4)
    circuit.add_U1_gate(taiou[2], 0.4)
    circuit.add_CNOT_gate(taiou[0], taiou[2])

    circuit.add_X_gate(taiou[2])
    circuit.add_CNOT_gate(taiou[4], taiou[3])
    circuit.add_Y_gate(taiou[1])

    circuit.add_RX_gate(taiou[2], -1.2)
    circuit.add_Z_gate(taiou[4])
    circuit.add_H_gate(taiou[0])

    circuit.add_S_gate(taiou[1])
    circuit.add_CNOT_gate(taiou[4], taiou[2])

    circuit.add_CZ_gate(taiou[1], taiou[3])

    circuit.add_Sdag_gate(taiou[4])
    circuit.add_T_gate(taiou[0])
    circuit.add_Tdag_gate(taiou[1])

    input_strs = [
        "U(1.20000004768372,2.1,0.9) q[0];",
        "U(1.5707963267949,-0.5,1.20000004768372) q[3];",
        "U(1.400000005960464,0,0) q[1];",
        "U(0,0,0.400000005960464) q[6];",
        "CX q[1],q[6];",
        "CX q[0],q[1];",
        "CX q[1],q[6];",
        "CX q[0],q[1];",
        "U(3.14159265358979,0,3.14159265358979) q[6];",
        "CX q[1],q[2];",
        "U(3.14159265358979,1.5707963267949,1.5707963267949) q[3];",
        "U(1.20000004768372,-1.5707963267949,1.5707963267949) q[6];",
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

    (n_qubit, input_list) = str_to_gate(input_strs, "notput", remap_remove=False)
    tran_gates = tran_ouqu_multi(n_qubit, input_list)

    testcircuit = QuantumCircuit(7)
    for it in tran_gates:
        # print(it.get_name())
        # print(it)
        testcircuit.add_gate(it)

    # print(testcircuit)
    check_circuit(circuit, testcircuit)
