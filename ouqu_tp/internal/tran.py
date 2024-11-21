import cmath
import typing
from cmath import atan, isclose, phase, pi, sqrt
from logging import NullHandler, getLogger
from typing import List, Tuple

import numpy as np
import numpy.typing as npt
import qulacs
from qulacs import QuantumCircuit
from qulacs.gate import RX, RZ, DenseMatrix, Identity, X, merge, sqrtX

logger = getLogger(__name__)
logger.addHandler(NullHandler())


def tran_ouqu_single(
    input_gate: qulacs.QuantumGateBase,
) -> typing.List[qulacs.QuantumGateBase]:
    # 1qubitのDenseMatrixゲートを入力し、 阪大のList[gate]の形に合わせます
    fugouZ = -1

    if len(input_gate.get_target_index_list()) != 1:
        logger.error("input gate is not single")
        raise RuntimeError("input gate is not single")
    if len(input_gate.get_control_index_list()) != 0:
        logger.error("input gate have control qubit")
        raise RuntimeError("input gate have control qubit")
    matrix = input_gate.get_matrix()
    qubit = input_gate.get_target_index_list()[0]

    out_gates: typing.List[qulacs.QuantumGateBase] = []
    # Rz単騎
    if cmath.isclose(abs(matrix[0][0]), 1, abs_tol=1e-5):
        degA = phase(matrix[1][1] / matrix[0][0]) * fugouZ
        if isclose(degA, 0):
            return out_gates
        out_gates.append(RZ(qubit, degA))
        return out_gates

    # Rz X
    if isclose(abs(matrix[0][0]), 0, abs_tol=1e-5):
        degA = phase(matrix[1][0] / matrix[0][1]) * fugouZ
        out_gates.append(RZ(qubit, degA))
        out_gates.append(X(qubit))
        return out_gates

    # Rz sqrtX Rz

    if isclose(abs(matrix[0][0]), cmath.sqrt(0.5), abs_tol=1e-5):
        degA = (phase(matrix[0][1] / matrix[0][0]) + pi / 2) * fugouZ
        degB = (phase(matrix[1][0] / matrix[0][0]) + pi / 2) * fugouZ
        out_gates.append(RZ(qubit, degA))
        out_gates.append(sqrtX(qubit))
        out_gates.append(RZ(qubit, degB))
        return out_gates

    # Rz sqrtX Rz sqrtX Rz
    adbc_mto = (matrix[0][0] * matrix[1][1]) / (matrix[0][1] * matrix[1][0])
    adbc = abs(adbc_mto)
    degB_com = -2 * atan(sqrt(adbc))  # 0～-π
    degB = degB_com.real * fugouZ
    degA = phase(-matrix[0][1] / matrix[0][0]) * fugouZ
    degC = phase(-matrix[1][0] / matrix[0][0]) * fugouZ

    out_gates.append(RZ(qubit, degA))
    out_gates.append(sqrtX(qubit))
    out_gates.append(RZ(qubit, degB))
    out_gates.append(sqrtX(qubit))
    out_gates.append(RZ(qubit, degC))
    return out_gates


def tran_ouqu_multi(inputcircuit: QuantumCircuit) -> QuantumCircuit:
    n_qubit = inputcircuit.get_qubit_count()
    anscircuit = QuantumCircuit(n_qubit)
    bitSingleGates = []

    for i in range(n_qubit):
        bitSingleGates.append(Identity(i))
    gate_num = inputcircuit.get_gate_count()
    for i in range(gate_num):
        ingate = inputcircuit.get_gate(i)

        # 測定はスキップ
        if ingate.get_name() == "CPTP" or ingate.get_name() == "Instrument":
            # TODO: 測定の追加位置（bitSingleGatesはまとめているためここで測定を追加できない）
            # anscircuit.add_gate(ingate)
            continue

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
                for tuigate in tran_ouqu_single(bitSingleGates[i]):
                    anscircuit.add_gate(tuigate)
                bitSingleGates[i] = Identity(i)
            anscircuit.add_gate(ingate)

    for i in range(n_qubit):
        for tuigate in tran_ouqu_single(bitSingleGates[i]):
            anscircuit.add_gate(tuigate)

    # 測定の追加
    for i in range(gate_num):
        ingate = inputcircuit.get_gate(i)
        if ingate.get_name() == "CPTP" or ingate.get_name() == "Instrument":
            # print(f"tran_ouqu_multi ingate: {ingate}")
            # print(
            #     f"tran_ouqu_multi get_target_index_list: {ingate.get_target_index_list()}")
            anscircuit.add_gate(ingate)

    return anscircuit


def CRes(targetA: int, targetB: int) -> qulacs.QuantumGateBase:
    gate_mat = np.array(
        [[1, 0, -1.0j, 0], [0, 1, 0, 1.0j], [-1.0j, 0, 1, 0], [0, 1.0j, 0, 1]]
    )
    return DenseMatrix([targetA, targetB], gate_mat / sqrt(2))  # type:ignore


def CResdag(targetA: int, targetB: int) -> qulacs.QuantumGateBase:
    gate_mat = np.array(
        [[1, 0, 1.0j, 0], [0, 1, 0, -1.0j], [1.0j, 0, 1, 0], [0, -1.0j, 0, 1]]
    )
    return DenseMatrix([targetA, targetB], gate_mat / sqrt(2))  # type:ignore


def CNOT_to_CRes(inputcircuit: QuantumCircuit) -> QuantumCircuit:
    n_qubit = inputcircuit.get_qubit_count()
    # 元のゲートにCNOTゲートが入っていたら、CResゲートに変換する
    anscircuit = QuantumCircuit(n_qubit)
    gate_num = inputcircuit.get_gate_count()
    for i in range(gate_num):
        ingate = inputcircuit.get_gate(i)
        if ingate.get_name() == "CNOT":
            target = ingate.get_target_index_list()[0]
            control = ingate.get_control_index_list()[0]
            anscircuit.add_gate(RX(target, pi / 2))
            anscircuit.add_gate(CRes(control, target))
            anscircuit.add_gate(RZ(control, pi / 2))
        else:
            anscircuit.add_gate(ingate)
    return anscircuit


def check_is_CRes(ingate: qulacs.QuantumGateBase) -> bool:
    if not ingate.get_name() == "DenseMatrix":
        return False
    if len(ingate.get_target_index_list()) != 2:
        return False
    if len(ingate.get_control_index_list()) != 0:
        return False

    true_mat = np.array(
        [[1, 0, -1.0j, 0], [0, 1, 0, 1.0j], [-1.0j, 0, 1, 0], [0, 1.0j, 0, 1]]
    ) / sqrt(2)
    return np.allclose(true_mat, ingate.get_matrix())


def check_is_CResdag(ingate: qulacs.QuantumGateBase) -> bool:
    if not ingate.get_name() == "DenseMatrix":
        return False
    if len(ingate.get_target_index_list()) != 2:
        return False
    if len(ingate.get_control_index_list()) != 2:
        return False

    true_mat = np.array(
        [[1, 0, 1.0j, 0], [0, 1, 0, -1.0j], [1.0j, 0, 1, 0], [0, -1.0j, 0, 1]]
    ) / sqrt(2)
    return np.allclose(true_mat, ingate.get_matrix())


def tran_to_pulse_tyukan(
    inputcircuit_in: QuantumCircuit,
    Res_list: List[Tuple[int, int]],
    dt: float,
    OZ: float,
    OX: float,
    ORes: float,
    mergin: int = 0,
) -> Tuple[List[Tuple[int, int, int]], int]:
    RZome = dt * OZ
    RXome = dt * OX
    CResome = dt * ORes
    inputcircuit = inputcircuit_in.copy()
    n_qubit = inputcircuit.get_qubit_count()

    inputcircuit = CNOT_to_CRes(inputcircuit)
    inputcircuit = tran_ouqu_multi(inputcircuit)
    """
    「任意の1qubit回転 + CNOT,CRes 」でできたcircuitを、中間表現に直します。
    各パルスは、(ゲート番号、スタート時刻、ゲート長さ) を持ちます。
    ゲート長さは、回転角/omeです。

    「空白」を表すゲートも入れる、　(何もしない間にもデコヒーレンスは発生するので)
    ゲート番号は、ZZZZZXXXXXRRRRR...RRSSSSS のような定義をされる
    (Sは空白ゲートです)

    この段階で,ゲートの向きをqulacsではなく、標準基準に戻します
    """
    logger.debug(n_qubit)
    logger.debug(inputcircuit)
    bangou = np.zeros((n_qubit, n_qubit), int)
    for i in range(n_qubit):
        for j in range(n_qubit):
            bangou[i][j] = -1
    for i in range(len(Res_list)):
        (ppp, qqq) = Res_list[i]
        bangou[ppp][qqq] = i

    saigo_zikan = np.zeros(n_qubit, int)
    pulse_comp: List[Tuple[int, int, int]] = []
    gate_num = inputcircuit.get_gate_count()

    space_ban_start = n_qubit * 2 + len(Res_list)

    for i in range(gate_num):
        ingate = inputcircuit.get_gate(i)

        target = ingate.get_target_index_list()[0]
        if ingate.get_name() == "Z-rotation":
            matrix = ingate.get_matrix()
            angle = phase(matrix[1][1] / matrix[0][0])
            if angle < -1e-6:
                angle += pi * 2
            pulse_kaz = int(angle / (RZome * 2) + 0.5)
            if pulse_kaz > 0:
                pulse_comp.append((target, saigo_zikan[target], pulse_kaz))
                saigo_zikan[target] += pulse_kaz + mergin

        elif ingate.get_name() == "sqrtX":
            pulse_kaz = int(pi / 2 / (RXome * 2) + 0.5)
            pulse_comp.append((target + n_qubit, saigo_zikan[target], pulse_kaz))
            saigo_zikan[target] += pulse_kaz + mergin
        elif ingate.get_name() == "X":
            pulse_kaz = int(pi / (RXome * 2) + 0.5)
            pulse_comp.append((target + n_qubit, saigo_zikan[target], pulse_kaz))
            saigo_zikan[target] += pulse_kaz + mergin
        elif check_is_CRes(ingate):
            control = ingate.get_target_index_list()[0]
            target = ingate.get_target_index_list()[1]
            ban = bangou[control][target]
            if ban == -1:
                logger.error(f"({control},{target}) gate is not in Res_list")
            start = max(saigo_zikan[target], saigo_zikan[control])
            if saigo_zikan[target] < start:
                pulse_comp.append(
                    (
                        space_ban_start + target,
                        saigo_zikan[target],
                        start - saigo_zikan[target],
                    )
                )
            if saigo_zikan[control] < start:
                pulse_comp.append(
                    (
                        space_ban_start + control,
                        saigo_zikan[control],
                        start - saigo_zikan[control],
                    )
                )
            pulse_kaz = int(pi / (CResome * 4) + 0.5)
            pulse_comp.append((ban + n_qubit * 2, start, pulse_kaz))
            saigo_zikan[target] = start + pulse_kaz + mergin
            saigo_zikan[control] = start + pulse_kaz + mergin
        else:
            logger.error("this gate is not (RZ,sx,x,CRes)")
            logger.error(ingate)
            raise RuntimeError("this gate is not (RZ,sx,x,CRes)")
    for aaa in pulse_comp:
        logger.debug(aaa)

    T = int(np.amax(saigo_zikan))

    return (pulse_comp, T)


def tran_to_pulse(
    inputcircuit: QuantumCircuit,
    Res_list: List[Tuple[int, int]],
    dt: float,
    OZ: float,
    OX: float,
    ORes: float,
    mergin: int = 0,
) -> npt.NDArray[np.float64]:
    RZome = dt * OZ
    RXome = dt * OX
    CResome = dt * ORes

    (pulse_comp, T) = tran_to_pulse_tyukan(
        inputcircuit, Res_list, dt, OZ, OX, ORes, mergin
    )
    """
    ゲートパルス中間表現を関数内で取得し、それをnumpy array に直します。
    arrayは、[ゲート名+1][時間(1パルス単位)] の配列です。

    array[0][時間(1パルス単位)]は、 実時間の配列です。{0,dt,dt*2,dt*3...}
    """
    n_qubit = inputcircuit.get_qubit_count()

    result_pulse = np.zeros((n_qubit * 2 + len(Res_list) + 1, int(T)))

    for ple in pulse_comp:
        (gate_ban, start, time) = ple
        if gate_ban >= n_qubit * 2 + len(Res_list):
            continue  # 空白に対応するので
        omega = RZome
        if gate_ban >= n_qubit:
            omega = RXome
        if gate_ban >= n_qubit * 2:
            omega = CResome
        for j in range(start, time + start):
            result_pulse[gate_ban + 1][j] = omega
    for j in range(T):
        result_pulse[0][j] = dt * j
    return result_pulse


def pulse_to_circuit(
    n_qubit: int,
    pulse_array: npt.NDArray[np.float64],
    Res_list: List[Tuple[int, int]],
) -> QuantumCircuit:
    # パルス情報が与えられたとき、量子回路を実行する関数です
    anscircuit = QuantumCircuit(n_qubit)
    m_kaz = n_qubit * 2 + len(Res_list)
    renzoku = np.zeros(m_kaz)
    T = len(pulse_array[0])
    for i in range(T + 1):
        for j in range(m_kaz):
            if i < T and pulse_array[j + 1][i] > 1e-8:
                renzoku[j] += pulse_array[j + 1][i]
            elif renzoku[j] > 1e-8:
                if j < n_qubit:
                    # RZ gate
                    anscircuit.add_gate(RZ(j, -renzoku[j] * 2))
                elif j < n_qubit * 2:
                    anscircuit.add_gate(RX(j - n_qubit, -renzoku[j] * 2))
                else:
                    (control, target) = Res_list[j - n_qubit * 2]
                    anscircuit.add_gate(CRes(control, target))
                renzoku[j] = 0
    return anscircuit
