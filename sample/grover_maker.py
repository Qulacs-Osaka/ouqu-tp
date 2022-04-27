from qiskit import QuantumCircuit, assemble, Aer, transpile

# 初期化
import matplotlib.pyplot as plt
import numpy as np



# from https://qiskit.org/textbook/ja/ch-algorithms/grover.html
qc = QuantumCircuit(3)
qc.cz(0, 2)
qc.cz(1, 2)
oracle_ex3 = qc.to_gate()
oracle_ex3.name = "U$_\omega$"
def initialize_s(qc, qubits):
    """qcの 'qubits' にH-gate を適用"""
    for q in qubits:
        qc.h(q)
    return qc
def diffuser(nqubits):
    qc = QuantumCircuit(nqubits)
    # Hゲートで |s> -> |00..0> に変換
    for qubit in range(nqubits):
        qc.h(qubit)
    # Xゲートで |00..0> -> |11..1> に変換
    for qubit in range(nqubits):
        qc.x(qubit)
    # マルチ制御Zゲートをかけます
    qc.h(nqubits-1)
    qc.mct(list(range(nqubits-1)), nqubits-1)  # マルチ制御トフォリ
    qc.h(nqubits-1)
    # |11..1> -> |00..0> に変換
    for qubit in range(nqubits):
        qc.x(qubit)
    # |00..0> -> |s> に変換
    for qubit in range(nqubits):
        qc.h(qubit)
    # Diffuserをゲートにします
    U_s = qc.to_gate()
    U_s.name = "U$_s$"
    return U_s
n = 3
grover_circuit = QuantumCircuit(n)
grover_circuit = initialize_s(grover_circuit, [0,1,2])
grover_circuit.append(oracle_ex3, [0,1,2])
grover_circuit.append(diffuser(n), [0,1,2])
grover_circuit.measure_all()
grover_circuit.draw()
aer_sim = Aer.get_backend('aer_simulator')
transpiled_grover_circuit = transpile(grover_circuit, aer_sim)
qobj = assemble(transpiled_grover_circuit)
results = aer_sim.run(qobj).result()
counts = results.get_counts()
#print(counts)
print(grover_circuit.qasm())

"""

# """