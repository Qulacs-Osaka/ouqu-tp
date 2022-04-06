
import typing
from cmath import phase

import qulacs
from qulacs.gate import CNOT, U3

#qelib1.inc にあるゲートのほとんどにqulacsを対応させる

#まずは、qulacs to QASM
def qulacs_to_QASM(cir :qulacs.Quantumcircit) -> None:
    # QASM風です
    # 

    # 気を付けて　qreg情報はない
    print("QulacsQASM 9.9")
    for kai in range(cir.get_gate_count()):
        # print(it.get_name())
        it = cir.get_gate(kai)
        clis=it.get_target_index_list()
        tlis=it.get_target_index_list()

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
        elif it.get_name() == "Z-rotation":
            matrix = it.get_matrix()
            angle = phase(matrix[1][1] / matrix[0][0])
            target=tlis[0]
            if abs(angle) > 1e-5:
                print(f"u1({angle}) q[{target}];")
        elif it.get_name() == "X":
            print("X q[", it.get_target_index_list()[0], "];")
        elif it.get_name() == "sqrtX":
            print("sx q[", it.get_target_index_list()[0], "];")
        else:
            print(it)  # 直接プリントできるらしい、　困ったらそうするしかない
    return
