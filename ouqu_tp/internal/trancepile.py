# from ouqu_tp.debug import check_circuit
from ouqu_tp.internal.ot_io import (
    input_strings,
    output_gates_QASMfuu,
    str_to_gate,
)
from ouqu_tp.internal.tran import tran_ouqu_multi

input_strs = input_strings()
(n_qubit, input_list) = str_to_gate(input_strs, "put", remap_remove=False)
tran_gates = tran_ouqu_multi(n_qubit, input_list)
output_gates_QASMfuu(tran_gates)


# ここからメモ
# やっぱりこの形式はやめて、qulacs.QuantumGateBaseを受け渡しすることになった
# staq -S -O2 -m --device qasm/ibm_tokyo.json --evaluate-all qasm/test_watle.qasm
