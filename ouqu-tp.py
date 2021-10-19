import cmath
from cmath import atan, isclose, phase, pi, sqrt

import numpy as np
from qulacs import QuantumCircuit, QuantumState
from qulacs.gate import CNOT, RZ, U3, Identity, X, merge, sqrtX


def tran_ouqu(input_gate):
    # print(input_gate)
    # 1qubitのDenseMatrixゲートを入力し、 阪大のList[gate]の形に合わせます
    if len(input_gate.get_target_index_list()) != 1:
        print("input gate is not single")
    if len(input_gate.get_control_index_list()) != 0:
        print("input gate have control qubit")
    matrix = input_gate.get_matrix()
    eps = 1e-7

    qubit = input_gate.get_target_index_list()[0]

    out_gates = []
    # Rz単騎
    if cmath.isclose(abs(matrix[0][0]), 1):
        degA = phase(matrix[1][1] / matrix[0][0])
        if isclose(degA, 0):
            return out_gates
        out_gates.append(["RZ", qubit, degA])
        return out_gates

    # Rz X
    if isclose(abs(matrix[0][0]), 0):
        degA = phase(matrix[1][0] / matrix[0][1])
        out_gates.append(["RZ", qubit, degA])
        out_gates.append(["X", qubit])
        return out_gates

    # Rz sqrtX Rz
    if isclose(abs(matrix[0][0]), cmath.sqrt(0.5)):
        degA = phase(matrix[1][0] / matrix[0][0]) + pi / 2
        degB = phase(matrix[0][1] / matrix[0][0]) + pi / 2
        out_gates.append(["RZ", qubit, degA])
        out_gates.append(["sqrtX", qubit])
        out_gates.append(["RZ", qubit, degB])
        return out_gates

    # Rz sqrtX Rz sqrtX Rz
    adbc = abs((matrix[0][0] * matrix[1][1]) / (matrix[0][1] * matrix[1][0]))
    # print(adbc)
    degB_com = 2 * atan(sqrt(adbc))
    # print(degB_com)
    degB = degB_com.real
    degA = phase(matrix[1][0] / matrix[0][0])
    degC = phase(matrix[0][1] / matrix[0][0])
    out_gates.append(["RZ", qubit, degA])
    out_gates.append(["sqrtX", qubit])
    out_gates.append(["RZ", qubit, degB])
    out_gates.append(["sqrtX", qubit])
    out_gates.append(["RZ", qubit, degC])
    return out_gates


def output_gates(gates):
    for it in gates:

        if it[0] == "RZ":
            print(it[0], it[1], it[2])
        if it[0] == "X":
            print(it[0], it[1])
        if it[0] == "sqrtX":
            print(it[0], it[1])
        if it[0] == "CNOT":
            print(it[0], it[1], it[2])
    return


def gates_to_circuit(gates, n_qubit):
    # watle形式を、qulacsのgate形式に変換する
    circuit = QuantumCircuit(n_qubit)
    for it in gates:
        if it[0] == "RZ":
            circuit.add_RZ_gate(it[1], it[2])
        if it[0] == "X":
            circuit.add_X_gate(it[1])
        if it[0] == "sqrtX":
            circuit.add_sqrtX_gate(it[1])
        if it[0] == "CNOT":
            circuit.add_CNOT_gate(it[1], it[2])
    return circuit


# ここからmain文

input_strs = []
while True:
    try:
        line = input()
        if line == "END":  # END という3文字を受け取る
            break
        input_strs.append(line)
    except EOFError:
        break

# input_list=[["U",0.0,0.0,0.785398,1],["CX",0,1],["U",0.0,0.0,0.785398,1]]
# この形式なんて言おう
# sinple argument gage
# SAG形式

input_list = []
n_qubit = 20  # 暫定
for instr in input_strs:
    if instr[0:7] == "qreg q[":
        mytable = instr.maketrans("qreg[];", "       ")
        yomustr = instr.translate(mytable)
        kazstr = yomustr.split(",")
        n_qubit = int(kazstr[0])
    if instr[0:2] == "U(":
        mytable = instr.maketrans("U()q[];", "   ,   ")
        yomustr = instr.translate(mytable)
        # print(yomustr)
        kazstr = yomustr.split(",")
        now_input = ["U"]
        now_input.append(float(kazstr[0]))
        now_input.append(float(kazstr[1]))
        now_input.append(float(kazstr[2]))
        now_input.append(int(kazstr[3]))
        input_list.append(now_input)

    if instr[0:2] == "CX":
        mytable = instr.maketrans("CXq[];", "      ")
        yomustr = instr.translate(mytable)
        # print(yomustr)
        kazstr = yomustr.split(",")
        now_input = ["CX"]
        now_input.append(int(kazstr[0]))
        now_input.append(int(kazstr[1]))
        input_list.append(now_input)

# staq -S -O2 -m --device qasm/ibm_tokyo.json --evaluate-all qasm/test_watle.qasm
# print(input_list)

bitSingleGates = []
tran_gates = []
for i in range(n_qubit):
    bitSingleGates.append(Identity(i))

for input in input_list:
    if input[0] == "U":
        newgate = merge(
            bitSingleGates[input[4]], U3(input[4], input[1], input[2], input[3])
        )
        bitSingleGates[input[4]] = newgate
    else:
        control = input[1]
        target = input[2]
        tran_gates += tran_ouqu(bitSingleGates[control])
        bitSingleGates[control] = Identity(control)
        tran_gates += tran_ouqu(bitSingleGates[target])
        bitSingleGates[target] = Identity(target)
        tran_gates.append(["CNOT", control, target])

for i in range(n_qubit):
    tran_gates += tran_ouqu(bitSingleGates[i])

output_gates(tran_gates)
# print(len(tran_gates))
# print(gates_to_circuit(tran_gates,n_qubit))
