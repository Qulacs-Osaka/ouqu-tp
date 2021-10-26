from ouqu_tp.ioSAG import input_strings, output_gates, str_to_gate
from ouqu_tp.tran import tran_ouqu_multi

# from ouqu_tp import input_strings,str_to_SAG,tran_ouqu_multi,output_gates

# ここからmain文
input_strs = input_strings()
(n_qubit, input_list) = str_to_gate(input_strs)
tran_gates = tran_ouqu_multi(n_qubit, input_list)
output_gates(tran_gates)


# ここからメモ
# 　次回　動くかどうかテスト
# input_list=[["U",0.0,0.0,0.785398,1],["CX",0,1],["U",0.0,0.0,0.785398,1]]
# やっぱりこの形式はやめて、qulacs.gateを受け渡しすることになった
# staq -S -O2 -m --device qasm/ibm_tokyo.json --evaluate-all qasm/test_watle.qasm
#
#
# test_kairo_Aが通らない　なぜ？ Zの回転方向？　その他のミス?
# fugouZ
# Z の回転方向調べる
# "qulacs.gate" は、型名ではないので、なおす
