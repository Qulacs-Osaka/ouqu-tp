import matplotlib.pyplot as plt
import numpy as np
import time 
import random
import math
import tqdm
from qulacs import PauliOperator, Observable, QuantumState,GeneralQuantumOperator
#GPU版をインストールしている場合のみ
#from qulacs import QuantumStateGpu
from qulacs import QuantumCircuit
from qulacs.gate import DenseMatrix , X,RX,RY
from qulacs.circuit import QuantumCircuitOptimizer
from qulacs.state import inner_product
from qulacs.gate import *
from qulacs import ParametricQuantumCircuit

def show_observable(hamiltonian):
    for j in range(hamiltonian.get_term_count()):
        pauli=hamiltonian.get_term(j)

        # Get the subscript of each pauli symbol
        index_list = pauli.get_index_list()

        # Get pauli symbols (I,X,Y,Z -> 0,1,2,3)
        pauli_id_list = pauli.get_pauli_id_list()

        # Get pauli coefficient
        coef = pauli.get_coef()

        # Create a copy of pauli operator
        another_pauli = pauli.copy()

        s = ["I","X","Y","Z"]
        pauli_str = [s[i] for i in pauli_id_list]
        terms_str = [item[0]+str(item[1]) for item in zip(pauli_str,index_list)]
        full_str = str(coef) + " " + " ".join(terms_str)
        print(full_str)

def ensemble_avarage(hairetu,sampling_num,sycle):
    return_hairetu=[]
    for i in range(int(sycle)):
        sigma_sum = 0
        for h in range(sampling_num):
            sigma_sum = sigma_sum + hairetu[h][i]
        sigma_sum = sigma_sum / sampling_num
        return_hairetu.append(sigma_sum)
    return return_hairetu

nqubits = 4
dt = 0.025
rep = 10
time = 25
num_steps = int(time/(rep*dt))
time_ax = np.arange(0,time,rep*dt)
num_samples = 200

#ハミルトニアンの定義
hamiltonian = [Observable(nqubits) for i in range(nqubits)]
"""
for i in range(nqubits):
    hamiltonian[i].add_operator(1., "Y {0}".format(i))
"""
#show_observable(hamiltonian)

# decay rateのリスト
decay_rate_amp = 0.6
decay_rate_ph = 0.06

pauli_ops = [PauliOperator("X 0",1),PauliOperator("Y 0",1),PauliOperator("Z 0",1)]

# jump operator のDenseMatrix gateのリスト


noisy_operation =[]
for i in range(nqubits):
    jump_op_list = [GeneralQuantumOperator(nqubits)  for i in range(2)]
    jump_op_list[0].add_operator(decay_rate_ph, "Z {0}".format(i))
    jump_op_list[1].add_operator(decay_rate_amp/2*1j, "Y {0}".format(i))
    jump_op_list[1].add_operator(decay_rate_amp/2, "X {0}".format(i))
    noisy_operation.append(NoisyEvolution(hamiltonian[i], jump_op_list, rep*dt, dt) )  

pauli_expect_val_list_ensamble = [[] for i in range(len(pauli_ops))]
pauli_ave = [[] for i in range(len(pauli_ops))]

for _ in tqdm.tqdm(range(num_samples)):
    state = QuantumState(nqubits)
    RY(0,np.pi/2).update_quantum_state(state)

    pauli_expect_val_list = [[] for i in range(len(pauli_ops))]
    
    for k in range(len(pauli_ops)):
        pauli_expect_val_list[k].append(pauli_ops[k].get_expectation_value(state).real)       
    
    for i in range(num_steps):
        noisy_operation[0].update_quantum_state(state)
        noisy_operation[1].update_quantum_state(state)
        noisy_operation[2].update_quantum_state(state)
        noisy_operation[3].update_quantum_state(state)
        for k in range(len(pauli_ops)):
            pauli_expect_val_list[k].append(pauli_ops[k].get_expectation_value(state).real)       


    for k in range(len(pauli_ops)):
        pauli_expect_val_list_ensamble[k].append(pauli_expect_val_list[k])#１回分の配列をここに入れる。
    
for k in range(len(pauli_ops)):
    pauli_ave[k] = ensemble_avarage( pauli_expect_val_list_ensamble[k] ,num_samples,num_steps)
    plt.plot(time_ax,pauli_ave[k],'.',label=f"qulacs_pauli{k}")

plt.legend()
plt.xlabel("time")
plt.ylabel("pauli expectation values")
plt.show()

