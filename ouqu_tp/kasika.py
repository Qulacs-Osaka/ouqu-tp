from qiskit import QuantumCircuit

input_circuit = QuantumCircuit.from_qasm_file("sample/input.qasm")
input_circuit.draw(output="mpl").savefig("sample/input_qasm_graph.png")
output_circuit = QuantumCircuit.from_qasm_file("sample/output.qasm")
output_circuit.draw(output="mpl").savefig("sample/output_qasm_graph.png")
