import cmath
import typing
from cmath import atan, isclose, phase, pi, sqrt

import qulacs
from qulacs.gate import RZ, Identity, X, merge, sqrtX


def tran_ouqu_single(
    input_gate: qulacs.QuantumGateBase,
) -> typing.List[qulacs.QuantumGateBase]:
    # print(input_gate)
    # 1qubitのDenseMatrixゲートを入力し、 阪大のList[gate]の形に合わせます
    fugouZ = -1

    if len(input_gate.get_target_index_list()) != 1:
        print("input gate is not single")
        return []
    if len(input_gate.get_control_index_list()) != 0:
        print("input gate have control qubit")
        return []
    matrix = input_gate.get_matrix()
    qubit = input_gate.get_target_index_list()[0]

    out_gates: typing.List[qulacs.QuantumGateBase] = []
    # Rz単騎
    if cmath.isclose(abs(matrix[0][0]), 1):
        degA = phase(matrix[1][1] / matrix[0][0]) * fugouZ
        # print(degA)
        if isclose(degA, 0):
            return out_gates
        out_gates.append(RZ(qubit, degA))
        return out_gates

    # Rz X
    if isclose(abs(matrix[0][0]), 0):

        degA = phase(matrix[1][0] / matrix[0][1]) * fugouZ
        # print(degA,"X")
        out_gates.append(RZ(qubit, degA))
        out_gates.append(X(qubit))
        return out_gates

    # Rz sqrtX Rz

    if isclose(abs(matrix[0][0]), cmath.sqrt(0.5)):
        degA = (phase(matrix[0][1] / matrix[0][0]) + pi / 2) * fugouZ
        degB = (phase(matrix[1][0] / matrix[0][0]) + pi / 2) * fugouZ
        # print(degA,degB)
        out_gates.append(RZ(qubit, degA))
        out_gates.append(sqrtX(qubit))
        out_gates.append(RZ(qubit, degB))
        return out_gates

    # Rz sqrtX Rz sqrtX Rz
    adbc_mto = (matrix[0][0] * matrix[1][1]) / (matrix[0][1] * matrix[1][0])
    # print(adbc_mto)
    adbc = abs(adbc_mto)
    # print(adbc)
    degB_com = -2 * atan(sqrt(adbc))  # 0～-π
    # print(degB_com)
    degB = degB_com.real * fugouZ
    degA = phase(-matrix[0][1] / matrix[0][0]) * fugouZ
    degC = phase(-matrix[1][0] / matrix[0][0]) * fugouZ

    # degC=1.045
    # 1.045周辺
    # print(degA,degB,degC)
    # print(matrix)
    # print(tan(degB_com/2))
    out_gates.append(RZ(qubit, degA))
    out_gates.append(sqrtX(qubit))
    out_gates.append(RZ(qubit, degB))
    out_gates.append(sqrtX(qubit))
    out_gates.append(RZ(qubit, degC))
    return out_gates


# 1.02判定でなにかある?
def tran_ouqu_multi(
    n_qubit: int, input_list: typing.List[qulacs.QuantumGateBase]
) -> typing.List[qulacs.QuantumGateBase]:
    bitSingleGates = []
    tran_gates = []

    for i in range(n_qubit):
        bitSingleGates.append(Identity(i))

    for ingate in input_list:
        if (
            len(ingate.get_control_index_list()) + len(ingate.get_target_index_list())
            <= 1
        ):
            target = ingate.get_target_index_list()[0]
            newgate = merge(bitSingleGates[target], ingate)
            bitSingleGates[target] = newgate
        else:
            bits = ingate.get_control_index_list() + ingate.get_target_index_list()
            for i in bits:
                tran_gates += tran_ouqu_single(bitSingleGates[i])
                bitSingleGates[i] = Identity(i)
            tran_gates.append(ingate)

    for i in range(n_qubit):
        tran_gates += tran_ouqu_single(bitSingleGates[i])

    return tran_gates
