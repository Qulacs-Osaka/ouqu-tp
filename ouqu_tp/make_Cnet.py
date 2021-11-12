from ot_io import input_strings

"""

解説


1行目：名前 なんでもいい
2行目:qubit数
3行目:connected数? (実は使ってない)
以降、connected数行:  control,tergetの順

例:
test
9
12
0,1
1,2
3,4
4,5
6,7
7,8
0,3
3,6
1,4
4,7
2,5
5,8


これは、
0-1-2
| | |
3-4-5
| | |
6-7-8
"""

input_strs = input_strings()
qubit_num = int(input_strs[1])
connect_num = int(input_strs[2])
con = []

print("{")
print('  "couplings": [')
for i in range(3, len(input_strs)):
    kazstr = input_strs[i].split(",")
    con.append([int(kazstr[0]), int(kazstr[1])])
    print("    {")
    print('      "control": ' + kazstr[0] + ",")
    print('      "target": ' + kazstr[1])
    if i + 1 < len(input_strs):
        print("    },")
    else:
        print("    }")
print("  ],")
print('  "name": "' + input_strs[0] + '",')
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
