import typing
from cmath import phase

import qulacs
from qulacs.gate import CNOT, U3


def input_strings() -> typing.List[str]:
    input_strs = []
    while True:
        try:
            line = input()
            if line == "END":  # END という3文字を受け取る
                break
            input_strs.append(line)
        except EOFError:
            break
    return input_strs


def str_to_gate(
    input_strs: typing.List[str], outmode: str
) -> typing.Tuple[int, typing.List[qulacs.QuantumGateBase]]:
    n_qubit: int = 0  # 暫定
    input_list: typing.List[qulacs.QuantumGateBase] = []
    for instr in input_strs:
        if instr[0:7] == "qreg q[":
            mytable = instr.maketrans("qreg[];", "       ")
            yomustr = instr.translate(mytable)
            kazstr = yomustr.split(",")
            n_qubit = int(kazstr[0])

        elif instr[0:2] == "U(":
            mytable = instr.maketrans("U()q[];", "   ,   ")
            yomustr = instr.translate(mytable)
            # print(yomustr)
            kazstr = yomustr.split(",")
            newgate = U3(
                int(kazstr[3]), float(kazstr[0]), float(kazstr[1]), float(kazstr[2])
            )
            input_list.append(newgate)
            if n_qubit < int(kazstr[3]) + 1:
                n_qubit = int(kazstr[3]) + 1

        elif instr[0:2] == "CX":
            mytable = instr.maketrans("CXq[];", "      ")
            yomustr = instr.translate(mytable)
            # print(yomustr)
            kazstr = yomustr.split(",")
            newgate = CNOT(int(kazstr[0]), int(kazstr[1]))
            input_list.append(newgate)

            if n_qubit < int(kazstr[0]) + 1:
                n_qubit = int(kazstr[0]) + 1
            if n_qubit < int(kazstr[1]) + 1:
                n_qubit = int(kazstr[1]) + 1

        elif outmode == "put":
            print(instr)
    return (n_qubit, input_list)


def output_gates(gates: typing.List[qulacs.QuantumGateBase]) -> None:
    # gateが直接渡されるようになった
    # print(gates)
    # print("OPENQASM 2.0")

    # 気を付けて　qreg情報はない
    for it in gates:
        # print(it.get_name())
        if it.get_name() == "Z-rotation":
            matrix = it.get_matrix()
            angle = phase(matrix[1][1] / matrix[0][0])
            print("RZ", it.get_target_index_list()[0], angle)
        elif it.get_name() == "X":
            print("X", it.get_target_index_list()[0])
        elif it.get_name() == "sqrtX":
            print("sqrtX", it.get_target_index_list()[0])
        elif it.get_name() == "CNOT":
            print("CNOT", it.get_control_index_list()[0], it.get_target_index_list()[0])
        else:
            print(it)  # 直接プリントできるらしい、　困ったらそうするしかない
    return


def output_gates_QASMfuu(gates: typing.List[qulacs.QuantumGateBase]) -> None:
    # QASM風です
    # print("OPENQASM 2.0")

    # 気を付けて　qreg情報はない

    for it in gates:
        # print(it.get_name())
        if it.get_name() == "Z-rotation":
            matrix = it.get_matrix()
            angle = phase(matrix[1][1] / matrix[0][0])
            print("u1(", angle, ") q[", it.get_target_index_list()[0], "]")
        elif it.get_name() == "X":
            print("X q[", it.get_target_index_list()[0], "]")
        elif it.get_name() == "sqrtX":
            print("sx q[", it.get_target_index_list()[0], "]")
        elif it.get_name() == "CNOT":
            print(
                "cx q[",
                it.get_control_index_list()[0],
                "] q[",
                it.get_target_index_list()[0],
                "]",
            )
        else:
            print(it)  # 直接プリントできるらしい、　困ったらそうするしかない
    return
