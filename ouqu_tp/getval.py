from typing import List

from qulacs import QuantumCircuit, QuantumState, observable

from ouqu_tp.ot_io import str_to_gate


def getval_do(input_strs: List[str], ferfile: str) -> float:
    (n_qubit, input_list) = str_to_gate(input_strs, "notput")
    print(n_qubit)
    # input_listを直接ぶち込む
    testcircuit = QuantumCircuit(n_qubit)
    for it in input_list:
        testcircuit.add_gate(it)
    out_state = QuantumState(n_qubit)
    testcircuit.update_quantum_state(out_state)

    obs = observable.create_observable_from_openfermion_file(ferfile)

    return float(obs.get_expectation_value(out_state))
    #qulacsの型アノテーションないので、怒りのキャスト
