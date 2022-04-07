import typing
from cmath import phase
from operator import truediv

import numpy as np
import qulacs
from parse import *
from qulacs import (
    Observable,
    ParametricQuantumCircuit,
    QuantumCircuit,
    QuantumState,
)
from qulacs.gate import CNOT, U3, DenseMatrix


def can_get_dence(gate):
    # dencematrixにできるかの関数
    return True


# qelib1.inc にあるゲートのほとんどにqulacsを対応させる
# sqrtYはない
# まずは、qulacs to QASM


def qulacs_to_QASM(cir) -> None:
    # QASM風です
    #

    # 気を付けて　qreg情報はない
    print("QulacsQASM Q.9")
    for kai in range(cir.get_gate_count()):
        # print(it.get_name())
        it = cir.get_gate(kai)
        clis = it.get_control_index_list()
        tlis = it.get_target_index_list()

        if it.get_name() == "CNOT":
            print(f"cx q[{clis[0]}],q[{tlis[0]}];")
        elif it.get_name() == "CZ":
            print(f"cz q[{clis[0]}],q[{tlis[0]}];")
        elif it.get_name() == "SWAP":
            print(f"swap q[{tlis[0]}],q[{tlis[1]}];")
        elif it.get_name() == "I":
            print(f"id q[{tlis[0]}];")
        elif it.get_name() == "X":
            print(f"x q[{tlis[0]}];")
        elif it.get_name() == "Y":
            print(f"y q[{tlis[0]}];")
        elif it.get_name() == "Z":
            print(f"z q[{tlis[0]}];")
        elif it.get_name() == "H":
            print(f"h q[{tlis[0]}];")
        elif it.get_name() == "S":
            print(f"s q[{tlis[0]}];")
        elif it.get_name() == "Sdag":
            print(f"sdg q[{tlis[0]}];")
        elif it.get_name() == "T":
            print(f"t q[{tlis[0]}];")
        elif it.get_name() == "Tdag":
            print(f"tdg q[{tlis[0]}];")
        elif it.get_name() == "sqrtX":
            print(f"sx q[{tlis[0]}];")
        elif it.get_name() == "sqrtXdag":
            print(f"sxdg q[{tlis[0]}];")
        elif it.get_name() == "X-rotation":
            matrix = it.get_matrix()
            angle = phase(matrix[0][0] - matrix[1][0]) * 2
            target = tlis[0]
            if abs(angle) > 1e-5:
                print(f"u1({angle}) q[{target}];")
        elif it.get_name() == "Y-rotation":
            matrix = it.get_matrix()
            angle = phase(matrix[0][0] + matrix[1][0] * 1.0j) * 2
            target = tlis[0]
            if abs(angle) > 1e-5:
                print(f"u1({angle}) q[{target}];")
        elif it.get_name() == "Z-rotation":
            matrix = it.get_matrix()
            angle = phase(matrix[1][1] / matrix[0][0])
            target = tlis[0]
            if abs(angle) > 1e-5:
                print(f"u1({angle}) q[{target}];")
        else:
            bit = len(it.get_target_index_list())
            matrix = it.get_matrix()
            print("DenseMatrix(", end="")
            print(len(it.get_target_index_list()), end="")
            print(",", end="")
            print(len(it.get_control_index_list()), end="")
            for i in range(2 ** bit):
                for j in range(2 ** bit):
                    print(",", end="")
                    print(matrix[i][j].real, end="")
                    print(",", end="")
                    print(matrix[i][j].imag, end="")
            for i in range(len(it.get_control_index_list())):
                print(",0", end="")  # control_valueが取得できないのでこうなった　あとで修正する

            print(") ", end="")
            for aaa in it.get_target_index_list():
                if aaa == it.get_target_index_list()[0]:
                    print(f"q[{aaa}]", end="")
                else:
                    print(f",q[{aaa}]", end="")
            for aaa in it.get_control_index_list():
                print(f",q[{aaa}]", end="")
            print(";")
        # get_matrix が効かないゲートの対応
        # 1qubitのDenseMatrixはu3ゲートに直すべきだが、やってない

    return


"""
  (0.707107,0)          (0,0) (-0,-0.707107)          (0,0)
         (0,0)   (0.707107,0)          (0,0)   (0,0.707107)
(-0,-0.707107)          (0,0)   (0.707107,0)          (0,0)
         (0,0)   (0,0.707107)          (0,0)   (0.707107,0)

DenseMatrix(2,1,0.707107,0,0,0,-0,-0.707107,0,0,0,0,0.707107,0,0,0,0,0.707107,-0,-0.707107,0,0,0.707107,0,0,0,0,0,0,0.707107,0,0,0.707107,0,1) q[0],q[1],q[2];
長すぎる

DenseMatrix(2,1
,0.707107,0,0,0,-0,-0.707107,0,0,0,0,0.707107,0,0,0,0,0.707107,-0,-0.707107,0,0,0.707107,0,0,0,0,0,0,0.707107,0,0,0.707107,0
,1)
q[0],q[1],q[2];
という風な改行の入れ方をする

パースする前に長さが決まるので、嬉しい


"""


def QASM_to_qulacs(input_strs: typing.List[str]) -> QuantumCircuit:
    # 仕様: キュービットレジスタはq[]のやつだけにしてください cregは無し
    n_qubit: int = 0  # 暫定
    cir = QuantumCircuit(2)
    for instr in input_strs:
        if instr[0:4] == "qreg":
            ary = parse("qreg q[{:d}];", instr)
            cir = QuantumCircuit(ary[0])
        elif instr[0:2] == "cx":
            ary = parse("cx q[{:d}],q[{:d}];", instr)
            cir.add_CNOT_gate(ary[0], ary[1])
        elif instr[0:2] == "cz":
            ary = parse("cz q[{:d}],q[{:d}];", instr)
            cir.add_CZ_gate(ary[0], ary[1])
        elif instr[0:4] == "swap":
            ary = parse("swap q[{:d}],q[{:d}];", instr)
            cir.add_SWAP_gate(ary[0], ary[1])
        elif instr[0:1] == "x":
            ary = parse("x q[{:d}];", instr)
            cir.add_X_gate(ary[0])
        elif instr[0:1] == "y":
            ary = parse("y q[{:d}];", instr)
            cir.add_Y_gate(ary[0])
        elif instr[0:1] == "z":
            ary = parse("z q[{:d}];", instr)
            cir.add_Z_gate(ary[0])
        elif instr[0:1] == "h":
            ary = parse("h q[{:d}];", instr)
            cir.add_H_gate(ary[0])
        elif instr[0:11] == "DenseMatrix":
            ary = search("DenseMatrix({:d},{:d}", instr)
            print(ary)
            parsestr = "DenseMatrix({:d},{:d}"
            for i in range(4 ** ary[0]):
                parsestr += ",{:g},{:g}"
            for i in range(ary[1]):
                parsestr += ",{:d}"
            parsestr += ") q[{:d}]"
            for i in range(ary[0] + ary[1] - 1):
                parsestr += ",q[{:d}]"
            parsestr += ";"
            print(parsestr)
            deary = parse(parsestr, instr)
            print(deary)
            gate_mat = np.zeros((2 ** ary[0], 2 ** ary[0]), dtype="complex")
            bas = 2
            for i in range(2 ** ary[0]):
                for j in range(2 ** ary[0]):
                    gate_mat[i][j] = deary[bas] + deary[bas + 1] * 1.0j
                    bas += 2
            control_values = []
            for i in range(ary[1]):
                control_values.append(deary[bas])
                bas += 1
            terget_indexes = []
            for i in range(ary[0]):
                terget_indexes.append(deary[bas])
                bas += 1

            dense_gate = DenseMatrix(terget_indexes, gate_mat)
            for i in range(ary[1]):
                control_index = deary[bas]
                bas += 1
                dense_gate.add_control_qubit(control_index, control_values[i])
            cir.add_gate(dense_gate)
    return cir
