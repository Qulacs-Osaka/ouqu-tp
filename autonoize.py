from typing import List, Tuple

from qulacs import QuantumCircuit, QuantumState

from qulacs.gate import IndependentXZNoise,TwoQubitDepolarizingNoise

from ouqu_tp.ot_io import str_to_gate

def autonoize(cir:QuantumCircuit,p1:float,p2:float,pm:float,pp:float)->QuantumCircuit:
    #cirを要素ごとに分解
    #その後、自動でnoizeを入れる
    n_qubit=cir.get_qubit_count()

    anscir=QuantumCircuit(n_qubit)
    
    #入力noize
    for i in range(n_qubit):
        anscir.add_gate(IndependentXZNoise(i,pm))
    
    for i in range(cir.get_gate_count()):
        ingate = cir.get_gate(i)
        anscir.add_gate(ingate)
        #ここで、ingateの種類によってnoizeする
    
