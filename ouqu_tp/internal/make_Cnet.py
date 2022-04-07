from typing import List, Tuple


def make_Cnet_put(input_strs: List[str]) -> None:
    qubit_num = int(input_strs[1])
    # connect_num = int(input_strs[2]) (not used)
    con = []

    print("{")
    print('  "couplings": [')
    for i in range(3, len(input_strs)):
        kazstr = input_strs[i].rstrip("\n").split(",")
        con.append([int(kazstr[0]), int(kazstr[1])])
        print("    {")
        print('      "control": ' + kazstr[0] + ",")
        print('      "target": ' + kazstr[1])
        if i + 1 < len(input_strs):
            print("    },")
        else:
            print("    }")
    print("  ],")
    print('  "name": "' + input_strs[0].rstrip("\n") + '",')
    print('  "qubits": [')
    for i in range(qubit_num):
        print("    {")
        print('      "id": ' + str(i))
        if i + 1 < qubit_num:
            print("    },")
        else:
            print("    }")
    print("  ]")
    print("}")


def get_connect(input_strs: List[str]) -> List[Tuple[int, int]]:
    con = []
    for i in range(3, len(input_strs)):
        kazstr = input_strs[i].rstrip("\n").split(",")
        con.append((int(kazstr[0]), int(kazstr[1])))
    return con
