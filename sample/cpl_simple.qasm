// Mapped to device "test"
// Qubits: 9
// Layout (physical --> virtual):
// 	q[0] --> q[0]
// 	q[1] --> q[2]
// 	q[2] --> q[1]
// 	q[3] --> 
// 	q[4] --> q[4]
// 	q[5] --> q[3]
// 	q[6] --> 
// 	q[7] --> 
// 	q[8] --> 
OPENQASM 2.0;
include "qelib1.inc";

qreg q[9];
U(0,0.20000004768372,0) q[0];