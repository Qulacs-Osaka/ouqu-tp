from qiskit import QuantumCircuit

input_circuit = QuantumCircuit.from_qasm_file("sample/grover_moto.qasm")
input_circuit.draw(output="mpl").savefig("sample/grover_moto._graph.png")
output_circuit = QuantumCircuit.from_qasm_file("sample/grover_cpl.qasm")
output_circuit.draw(output="mpl").savefig("sample/grover_cpl_graph.png")
