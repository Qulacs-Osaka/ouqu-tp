import cmath
import typing
from cmath import atan, isclose, phase, pi, sqrt
from turtle import pu
from xmlrpc.client import Boolean

import numpy as np
import qulacs
from qulacs import QuantumState
from qulacs.gate import RX, RZ, DenseMatrix, Identity, X, merge, sqrtX


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

    # print(degA,degB,degC)
    # print(matrix)
    # print(tan(degB_com/2))
    out_gates.append(RZ(qubit, degA))
    out_gates.append(sqrtX(qubit))
    out_gates.append(RZ(qubit, degB))
    out_gates.append(sqrtX(qubit))
    out_gates.append(RZ(qubit, degC))
    return out_gates


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


def CNOT_to_CRes(
    input_list: typing.List[qulacs.QuantumGateBase],
) -> typing.List[qulacs.QuantumGateBase]:
    # 元のゲートにCNOTゲートが入っていたら、CResゲートに変換する
    tran_gates = []
    for ingate in input_list:
        if ingate.get_name() == "CNOT":
            target = ingate.get_target_index_list()[0]
            control = ingate.get_control_index_list()[0]
            tran_gates.append(RX(target, pi / 2))
            gate_mat = np.array(
                [[1, 0, -1.0j, 0], [0, 1, 0, 1.0j], [-1.0j, 0, 1, 0], [0, 1.0j, 0, 1]]
            )
            tran_gates.append(DenseMatrix([control, target], gate_mat / sqrt(2)))
            tran_gates.append(RZ(control, pi / 2))
        else:
            tran_gates.append(ingate)
    return tran_gates


def check_is_CRes(ingate: qulacs.QuantumGateBase) -> bool:
    if not ingate.get_name() == "DenseMatrix":
        return False
    if len(ingate.get_target_index_list()) != 2:
        return False
    return True


def tran_to_pulse(
    n_qubit: int,
    input_list: typing.List[qulacs.QuantumGateBase],
    Res_list,
    RZome: float,
    RXome: float,
    CResome: float,
    mergin: int,
):
    input_list = CNOT_to_CRes(input_list)
    tran_gates = tran_ouqu_multi(n_qubit, input_list)

    # 回転角/ome　を整数に直した時間だけパルスが入る
    # 各回転操作に対して、　mergin の分だけ空白が入る
    # できるだけ短時間で行う

    # numpy arrayは[ゲート番号][時間]　で定義される
    # ゲート番号は、ZZZZZXXXXXRRRRR... のような定義をされる

    bangou = np.zeros((n_qubit, n_qubit), int)
    for i in range(n_qubit):
        for j in range(n_qubit):
            bangou[i][j] = -1
    for i in range(len(Res_list)):
        (ppp, qqq) = Res_list[i]
        bangou[ppp][qqq] = i

    saigo_zikan = np.zeros(n_qubit, int)
    pulse_comp = []
    for i in range(n_qubit * 2 + len(Res_list)):
        pulse_comp.append([])
    for it in tran_gates:

        target = it.get_target_index_list()[0]
        if it.get_name() == "Z-rotation":
            matrix = it.get_matrix()
            angle = -phase(matrix[1][1] / matrix[0][0])
            if angle < -1e-6:
                angle += pi * 2
            pulse_kaz = int(angle / (RZome * 2) + 0.5)
            if pulse_kaz > 0:
                pulse_comp[target].append((saigo_zikan[target], pulse_kaz))
                saigo_zikan[target] += pulse_kaz + mergin

        elif it.get_name() == "sqrtX":
            pulse_kaz = int(pi / 2 / (RXome * 2) + 0.5)
            pulse_comp[target + n_qubit].append((saigo_zikan[target], pulse_kaz))
            saigo_zikan[target] += pulse_kaz + mergin
        elif it.get_name() == "X":
            pulse_kaz = int(pi / (RXome * 2) + 0.5)
            pulse_comp[target + n_qubit].append((saigo_zikan[target], pulse_kaz))
            saigo_zikan[target] += pulse_kaz + mergin
        elif check_is_CRes(it):
            control = it.get_target_index_list()[0]
            target = it.get_target_index_list()[1]
            ban = bangou[control][target]
            if ban == -1:
                print("error")
            start = max(saigo_zikan[target], saigo_zikan[control])
            pulse_kaz = int(pi / (CResome * 4) + 0.5)
            pulse_comp[ban + n_qubit * 2].append((start, pulse_kaz))
            saigo_zikan[target] = start + pulse_kaz + mergin
            saigo_zikan[control] = start + pulse_kaz + mergin
        else:
            print("unknown gate ")
            print(it)
    for aaa in pulse_comp:
        print(aaa)
    T = np.amax(saigo_zikan)
    result_pulse = np.zeros((n_qubit * 2 + len(Res_list), int(T)))
    for i in range((n_qubit * 2 + len(Res_list))):
        omega = RZome
        if i >= n_qubit:
            omega = RXome
        if i >= n_qubit * 2:
            omega = CResome
        for ple in pulse_comp[i]:
            (start, time) = ple
            for j in range(start, time + start):
                result_pulse[i][j] = omega
    return result_pulse


def pulse_to_gate(
    n_qubit: int, pulse_array, Res_list
) -> typing.List[qulacs.QuantumGateBase]:
    # パルス情報が与えられたとき、量子回路を実行する関数です
    print(pulse_array)
    gates = []
    m_kaz = n_qubit * 2 + len(Res_list)
    renzoku = np.zeros(m_kaz)
    T = len(pulse_array[0])
    print(T)
    for i in range(T + 1):
        for j in range(m_kaz):
            if i < T and pulse_array[j][i] > 1e-8:
                renzoku[j] += pulse_array[j][i]
            elif renzoku[j] > 1e-8:
                if j < n_qubit:
                    # RZ gate
                    gates.append(RZ(j, renzoku[j] * 2))
                elif j < n_qubit * 2:
                    gates.append(RX(j - n_qubit, -renzoku[j] * 2))
                else:
                    (control, target) = Res_list[j - n_qubit * 2]
                    gate_mat = np.array(
                        [
                            [1, 0, -1.0j, 0],
                            [0, 1, 0, 1.0j],
                            [-1.0j, 0, 1, 0],
                            [0, 1.0j, 0, 1],
                        ]
                    )
                    gates.append(DenseMatrix([control, target], gate_mat / sqrt(2)))
                print(renzoku[j] * 2)
                renzoku[j] = 0
    return gates
