import typing
from cmath import phase

import numpy as np
from parse import parse, search
from qulacs import QuantumCircuit
from qulacs.gate import DenseMatrix


def can_get_dence(gate):
    # dencematrixにできるかの関数
    return True


# qelib1.inc にあるゲートのほとんどにqulacsを対応させる
# sqrtYはない
# まずは、qulacs to QASM


def qulacs_to_QASM(cir) -> typing.List[str]:
    # QASM風です
    #

    # 気を付けて　qreg情報はない
    out_strs = ["QulacsQASM Q.9", f"qreg q[{cir.get_qubit_count()}];"]

    for kai in range(cir.get_gate_count()):
        # #print(it.get_name())
        it = cir.get_gate(kai)
        clis = it.get_control_index_list()
        tlis = it.get_target_index_list()

        if it.get_name() == "CNOT":
            out_strs.append(f"cx q[{clis[0]}],q[{tlis[0]}];")
        elif it.get_name() == "CZ":
            out_strs.append(f"cz q[{clis[0]}],q[{tlis[0]}];")
        elif it.get_name() == "SWAP":
            out_strs.append(f"swap q[{tlis[0]}],q[{tlis[1]}];")
        elif it.get_name() == "I":
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
        else:
            now_string = ""
            bit = len(it.get_target_index_list())
            matrix = it.get_matrix()
            now_string += "DenseMatrix("
            now_string += str(len(it.get_target_index_list()))
            now_string += ","
            now_string += str(len(it.get_control_index_list()))
            for i in range(2 ** bit):
                for j in range(2 ** bit):
                    now_string += ","
                    now_string += str(matrix[i][j].real)
                    now_string += ","
                    now_string += str(matrix[i][j].imag)
            for i in range(len(it.get_control_index_list())):
                now_string += ",1"  # control_valueが取得できないのでこうなった　あとで修正する

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


def QASM_to_qulacs(input_strs: typing.List[str]) -> QuantumCircuit:
    # 仕様: キュービットレジスタはq[]のやつだけにしてください cregは無し
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
        elif instr[0:2] == "s ":
            ary = parse("s q[{:d}];", instr)
            cir.add_S_gate(ary[0])
        elif instr[0:4] == "sdg ":
            ary = parse("sdg q[{:d}];", instr)
            cir.add_Sdag_gate(ary[0])
        elif instr[0:2] == "t ":
            ary = parse("t q[{:d}];", instr)
            cir.add_T_gate(ary[0])
        elif instr[0:4] == "tdg ":
            ary = parse("tdg q[{:d}];", instr)
            cir.add_Tdag_gate(ary[0])
        elif instr[0:2] == "rx":
            ary = parse("rx({:g}) q[{:d}];", instr)
            cir.add_RX_gate(ary[1], -ary[0])
        elif instr[0:2] == "ry":
            ary = parse("ry({:g}) q[{:d}];", instr)
            cir.add_RY_gate(ary[1], -ary[0])
        elif instr[0:2] == "rz":
            ary = parse("rz({:g}) q[{:d}];", instr)
            cir.add_RZ_gate(ary[1], -ary[0])
        elif instr[0:11] == "DenseMatrix":
            ary = search("DenseMatrix({:d},{:d}", instr)
            # print(ary)
            parsestr = "DenseMatrix({:d},{:d}"
            for i in range(4 ** ary[0]):
                parsestr += ",{:g},{:g}"
            for i in range(ary[1]):
                parsestr += ",{:d}"
            parsestr += ") q[{:d}]"
            for i in range(ary[0] + ary[1] - 1):
                parsestr += ",q[{:d}]"
            parsestr += ";"
            # print(parsestr)
            deary = parse(parsestr, instr)
            # print(deary)
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
