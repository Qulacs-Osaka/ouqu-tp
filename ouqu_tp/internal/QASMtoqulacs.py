import typing
from cmath import phase
from logging import NullHandler, getLogger
from typing import List

import numpy as np
from parse import parse, search
from qulacs import QuantumCircuit, QuantumGateBase, QuantumState
from qulacs.gate import DenseMatrix, Identity, Measurement

from ouqu_tp.internal.tran import (
    CRes,
    CResdag,
    check_is_CRes,
    check_is_CResdag,
)

logger = getLogger(__name__)
logger.addHandler(NullHandler())


def can_get_dence(gate: QuantumGateBase) -> bool:
    # dencematrixにできるかの関数
    return True


# qelib1.inc にあるゲートのほとんどにqulacsを対応させる
# sqrtYはない
# まずは、qulacs to QASM


def qulacs_to_QASM(cir: QuantumCircuit) -> typing.List[str]:
    # QASM風です
    #

    out_strs = [
        "OPENQASM 2.0;",
        'include "qelib1.inc";',
        f"qreg q[{cir.get_qubit_count()}];",
        f"creg c[{cir.get_qubit_count()}];",
    ]

    for kai in range(cir.get_gate_count()):
        it = cir.get_gate(kai)
        clis = it.get_control_index_list()
        tlis = it.get_target_index_list()

        # print(f"it.get_name(): {it.get_name()}")

        if it.get_name() == "CNOT":
            out_strs.append(f"cx q[{clis[0]}],q[{tlis[0]}];")
        elif it.get_name() == "CZ":
            out_strs.append(f"cz q[{clis[0]}],q[{tlis[0]}];")
        elif it.get_name() == "SWAP":
            out_strs.append(f"swap q[{tlis[0]}],q[{tlis[1]}];")
        elif it.get_name() == "Identity":
            out_strs.append(f"id q[{tlis[0]}];")
        elif it.get_name() == "X":
            out_strs.append(f"x q[{tlis[0]}];")
        elif it.get_name() == "Y":
            out_strs.append(f"y q[{tlis[0]}];")
        elif it.get_name() == "Z":
            out_strs.append(f"z q[{tlis[0]}];")
        elif it.get_name() == "H":
            out_strs.append(f"h q[{tlis[0]}];")
        elif it.get_name() == "S":
            out_strs.append(f"s q[{tlis[0]}];")
        elif it.get_name() == "Sdag":
            out_strs.append(f"sdg q[{tlis[0]}];")
        elif it.get_name() == "T":
            out_strs.append(f"t q[{tlis[0]}];")
        elif it.get_name() == "Tdag":
            out_strs.append(f"tdg q[{tlis[0]}];")
        elif it.get_name() == "sqrtX":
            out_strs.append(f"sx q[{tlis[0]}];")
        elif it.get_name() == "sqrtXdag":
            out_strs.append(f"sxdg q[{tlis[0]}];")
        elif it.get_name() == "X-rotation":
            matrix = it.get_matrix()
            angle = phase(matrix[0][0] - matrix[1][0]) * 2
            if abs(angle) > 1e-5:
                out_strs.append(f"rx({angle}) q[{tlis[0]}];")
        elif it.get_name() == "Y-rotation":
            matrix = it.get_matrix()
            angle = phase(matrix[0][0] + matrix[1][0] * 1.0j) * 2
            if abs(angle) > 1e-5:
                out_strs.append(f"ry({angle}) q[{tlis[0]}];")
        elif it.get_name() == "Z-rotation":
            matrix = it.get_matrix()
            angle = phase(matrix[1][1] / matrix[0][0])
            if abs(angle) > 1e-5:
                out_strs.append(f"rz({angle}) q[{tlis[0]}];")
        elif it.get_name() == "CPTP":
            # TODO: classical_pos
            target_idx_list = it.get_target_index_list()
            if len(target_idx_list) > 0:
                target_idx = target_idx_list[0]
                out_strs.append(f"measure q[{target_idx}]->c[{target_idx}];")
        elif check_is_CRes(it):
            out_strs.append(f"CRes q[{tlis[0]}],q[{tlis[1]}];")
        elif check_is_CResdag(it):
            out_strs.append(f"CResdag q[{tlis[0]}],q[{tlis[1]}];")
        elif can_get_dence(it):
            now_string = ""
            bit = len(it.get_target_index_list())
            matrix = it.get_matrix()
            now_string += "DenseMatrix("
            now_string += str(len(it.get_target_index_list()))
            now_string += ","
            now_string += str(len(it.get_control_index_list()))
            for i in range(2**bit):
                for j in range(2**bit):
                    now_string += f",{matrix[i][j].real:.6g},{matrix[i][j].imag:.6g}"
            for i in range(len(it.get_control_index_list())):
                if it.get_control_value_list()[i] == 1:
                    now_string += ",1"
                else:
                    now_string += ",0"

            now_string += ") "
            for aaa in it.get_target_index_list():
                if aaa == it.get_target_index_list()[0]:
                    now_string += f"q[{aaa}]"
                else:
                    now_string += f",q[{aaa}]"
            for aaa in it.get_control_index_list():
                now_string += f",q[{aaa}]"
            now_string += ";"
            out_strs.append(now_string)
        else:
            out_strs.append("unknown gate:" + it.get_name())
            logger.warning("unknown gate:" + it.get_name())
            print(f"unknown gate: {it.get_name()}")
        # get_matrix が効かないゲートの対応
        # 1qubitのDenseMatrixはu3ゲートに直すべきだが、やってない

    return out_strs


"""
  (0.707107,0)          (0,0) (-0,-0.707107)          (0,0)
         (0,0)   (0.707107,0)          (0,0)   (0,0.707107)
(-0,-0.707107)          (0,0)   (0.707107,0)          (0,0)
         (0,0)   (0,0.707107)          (0,0)   (0.707107,0)

DenseMatrix(2,1,0.707107,0,0,0,-0,-0.707107,0,0,0,0,0.707107,0,0,0,0,0.707107,-0,-0.707107,0,0,0.707107,0,0,0,0,0,0,0.707107,0,0,0.707107,0,1) q[0],q[1],q[2];

"""


def QASM_to_qulacs(
    input_strs: typing.List[str], *, remap_remove: bool = False
) -> QuantumCircuit:
    # 仕様: キュービットレジスタはq[]のやつだけにしてください
    n = 0
    mapping: List[int] = []

    for instr_moto in input_strs:
        instr = instr_moto.lower().strip().replace(" ", "").replace("\t", "")
        # 全部小文字にして、前後の改行を削除、　すべての空白とタブを削除した状態でマッチングします
        if instr[0:4] == "qreg":
            ary = parse("qreg{v}[{n}];", instr)
            if ary is not None:
                n = int(ary["n"].strip())
                # v = ary["v"].strip()
                cir = QuantumCircuit(n)
                if len(mapping) == 0:
                    mapping = list(range(n))
        elif instr[0:4] == "creg":
            continue
        elif instr[0:4] == "gate":
            continue
        elif remap_remove and instr[0:4] == "//q[":
            ary = parse("//q[{:d}]-->q[{:d}]", instr)
            if ary is not None:
                mapping[ary[0]] = ary[1]
        elif remap_remove and instr[0:8] == "//qubits":
            ary = parse("//qubits:{:d}", instr)
            mapping = list(range(ary[0]))
        elif instr[0:2] == "//":
            continue
        elif instr.lower() == "openqasm2.0;":
            continue
        elif instr.lower() == 'include"qelib1.inc";':
            continue
        elif instr.isspace():
            continue
        elif instr == "}":
            continue
        elif instr == "":
            continue

        elif instr[0:2] == "cx":
            ary = parse("cxq[{:d}],q[{:d}];", instr)
            if ary is not None:
                cir.add_CNOT_gate(mapping[ary[0]], mapping[ary[1]])
        elif instr[0:2] == "cz":
            ary = parse("czq[{:d}],q[{:d}];", instr)
            cir.add_CZ_gate(mapping[ary[0]], mapping[ary[1]])
        elif instr[0:4] == "swap":
            ary = parse("swapq[{:d}],q[{:d}];", instr)
            cir.add_SWAP_gate(mapping[ary[0]], mapping[ary[1]])
        elif instr[0:2] == "id":
            ary = parse("idq[{:d}];", instr)
            cir.add_gate(Identity(mapping[ary[0]]))
        elif instr[0:2] == "xq":
            ary = parse("xq[{:d}];", instr)
            cir.add_X_gate(mapping[ary[0]])
        elif instr[0:2] == "yq":
            ary = parse("yq[{:d}];", instr)
            cir.add_Y_gate(mapping[ary[0]])
        elif instr[0:2] == "zq":
            ary = parse("zq[{:d}];", instr)
            cir.add_Z_gate(mapping[ary[0]])
        elif instr[0:2] == "hq":
            ary = parse("hq[{:d}];", instr)
            cir.add_H_gate(mapping[ary[0]])
        elif instr[0:2] == "sq":
            ary = parse("sq[{:d}];", instr)
            cir.add_S_gate(mapping[ary[0]])
        elif instr[0:4] == "sdgq":
            ary = parse("sdgq[{:d}];", instr)
            cir.add_Sdag_gate(mapping[ary[0]])
        elif instr[0:2] == "tq":
            ary = parse("tq[{:d}];", instr)
            cir.add_T_gate(mapping[ary[0]])
        elif instr[0:4] == "tdgq":
            ary = parse("tdgq[{:d}];", instr)
            cir.add_Tdag_gate(mapping[ary[0]])
        elif instr[0:2] == "rx":
            ary = parse("rx({:g})q[{:d}];", instr)
            cir.add_RX_gate(mapping[ary[1]], -ary[0])
        elif instr[0:2] == "ry":
            ary = parse("ry({:g})q[{:d}];", instr)
            cir.add_RY_gate(mapping[ary[1]], -ary[0])
        elif instr[0:2] == "rz":
            ary = parse("rz({:g})q[{:d}];", instr)
            cir.add_RZ_gate(mapping[ary[1]], -ary[0])
        elif instr[0:1] == "p":
            ary = parse("p({:g})q[{:d}];", instr)
            cir.add_U1_gate(mapping[ary[1]], ary[0])
        elif instr[0:2] == "u1":
            ary = parse("u1({:g})q[{:d}];", instr)
            cir.add_U1_gate(mapping[ary[1]], ary[0])
        elif instr[0:2] == "u2":
            ary = parse("u2({:g},{:g})q[{:d}];", instr)
            cir.add_U2_gate(mapping[ary[2]], ary[0], ary[1])
        elif instr[0:2] == "u3":
            ary = parse("u3({:g},{:g},{:g})q[{:d}];", instr)
            cir.add_U3_gate(mapping[ary[3]], ary[0], ary[1], ary[2])
        elif instr[0:1] == "u":
            ary = parse("u({:g},{:g},{:g})q[{:d}];", instr)
            if ary is not None:
                cir.add_U3_gate(mapping[ary[3]], ary[0], ary[1], ary[2])
        elif instr[0:3] == "sxq":
            ary = parse("sxq[{:d}];", instr)
            cir.add_sqrtX_gate(mapping[ary[0]])
        elif instr[0:5] == "sxdgq":
            ary = parse("sxdgq[{:d}];", instr)
            cir.add_sqrtXdag_gate(mapping[ary[0]])
        elif instr[0:5] == "cresq":
            ary = parse("CResq[{:d}],q[{:d}];", instr)
            cir.add_gate(CRes(mapping[ary[0]], mapping[ary[1]]))
        elif instr[0:8] == "cresdagq":
            ary = parse("CResdagq[{:d}],q[{:d}];", instr)
            cir.add_gate(CResdag(mapping[ary[0]], mapping[ary[1]]))
        elif instr[0:11] == "densematrix":
            ary = search("densematrix({:d},{:d}", instr)
            parsestr = "densematrix({:d},{:d}"
            for i in range(4 ** ary[0]):
                parsestr += ",{:g},{:g}"
            for i in range(ary[1]):
                parsestr += ",{:d}"
            parsestr += ")q[{:d}]"
            for i in range(ary[0] + ary[1] - 1):
                parsestr += ",q[{:d}]"
            parsestr += ";"
            deary = parse(parsestr, instr)
            gate_mat = np.zeros((2 ** ary[0], 2 ** ary[0]), dtype="complex")
            bas = 2
            for i in range(2 ** ary[0]):
                for j in range(2 ** ary[0]):
                    gate_mat[i][j] = deary[bas] + deary[bas + 1] * 1.0j
                    bas += 2
            control_values = []
            for i in range(ary[1]):
                control_values.append(mapping[deary[bas]])
                bas += 1
            terget_indexes = []
            for i in range(ary[0]):
                terget_indexes.append(mapping[deary[bas]])
                bas += 1

            dense_gate = DenseMatrix(terget_indexes, gate_mat)
            for i in range(ary[1]):
                control_index = deary[bas]
                bas += 1
                dense_gate.add_control_qubit(control_index, control_values[i])
            cir.add_gate(dense_gate)
        elif instr[0:7] == "measure":
            ary = parse("measure{q}->{c};", instr)
            if ary is not None:
                q = ary["q"].strip()
                c = ary["c"].strip()
                qary = parse("{s}[{:d}]", q)
                cary = parse("{s}[{:d}]", c)
                # print(f"qary: {qary}")
                # print(f"cary: {cary}")
                if qary is not None and cary is not None:
                    # print(f"qary[0]: {qary[0]}")
                    # print(f"cary[0]: {cary[0]}")
                    measurement_gate = Measurement(qary[0], cary[0])
                    # print(
                    #     f"measurement_gate.name: {measurement_gate.get_name()}")
                    # print(
                    #     f"measurement_gate get_target_index_list: {measurement_gate.get_target_index_list()}")
                    cir.add_gate(measurement_gate)
                else:
                    for i in range(n):
                        measurement_gate = Measurement(i, i)
                        cir.add_gate(measurement_gate)
        else:
            print("// unknown line:", instr)
    return cir


def state_to_strs(state: QuantumState) -> typing.List[str]:
    return state.to_string().split("\n")


def strs_to_state(strs: typing.List[str]) -> QuantumState:
    qubit = parse(" * Qubit Count : {:d}", strs[1])[0]
    Dim = 2**qubit
    state_vec: typing.List[complex] = [0.0 + 0.0j] * Dim
    for i in range(Dim):
        ary = search("({:g},{:g})", strs[4 + i])
        state_vec[i] = ary[0] + ary[1] * 1.0j
    state = QuantumState(qubit)
    state.load(state_vec)
    return state
