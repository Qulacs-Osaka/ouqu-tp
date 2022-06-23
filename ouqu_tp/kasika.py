from qiskit import Aer, QuantumCircuit, execute

input_circuit = QuantumCircuit.from_qasm_file("sample/input.qasm")
input_circuit.draw(output="mpl").savefig("sample/input_qasm_graph.png")
output_circuit = QuantumCircuit.from_qasm_file("sample/output.qasm")
output_circuit.draw(output="mpl").savefig("sample/output_qasm_graph.png")

vector_sim = Aer.get_backend("statevector_simulator")
job = execute(input_circuit, vector_sim)
ket = job.result().get_statevector()
for amplitude in ket:
    print(amplitude)

print()

job2 = execute(output_circuit, vector_sim)
ket2 = job2.result().get_statevector()

bit_narabe = [0, 2, 1, 5, 4]

naiseki = 0
for i in range(32):
    bit_ter = 0
    for j in range(5):
        if (i & (2**j)) > 0:
            bit_ter += 2 ** bit_narabe[j]

    print(ket2[bit_ter])

    naiseki += ket[i] * ket2[bit_ter].conj()

print(abs(naiseki))
