import cmath
from cmath import atan, isclose, phase, pi, sqrt

from qulacs import QuantumCircuit
from qulacs.gate import U3, Identity, merge
from ouqu_tp.ioSAG import input_strings,str_to_gate,output_gates
from ouqu_tp.tran import tran_ouqu_multi
#from ouqu_tp import input_strings,str_to_SAG,tran_ouqu_multi,output_gates

# ここからmain文
input_strs=input_strings()
(n_qubit,input_list)=str_to_gate(input_strs)
tran_gates=tran_ouqu_multi(n_qubit,input_list)
output_gates(tran_gates)


#ここからメモ
#　次回　動くかどうかテスト
# input_list=[["U",0.0,0.0,0.785398,1],["CX",0,1],["U",0.0,0.0,0.785398,1]]
# やっぱりこの形式はやめて、qulacs.gateを受け渡しすることになった
# staq -S -O2 -m --device qasm/ibm_tokyo.json --evaluate-all qasm/test_watle.qasm
#
#
#
