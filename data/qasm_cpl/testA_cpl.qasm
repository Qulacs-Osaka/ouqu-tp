// Mapped to device "20 qubit IBM Tokyo device"
// Qubits: 20
// Layout (physical --> virtual):
// 	q[0] --> q[0]
// 	q[1] --> q[4]
// 	q[2] --> q[3]
// 	q[3] --> q[1]
// 	q[4] --> 
// 	q[5] --> 
// 	q[6] --> q[2]
// 	q[7] --> 
// 	q[8] --> 
// 	q[9] --> 
// 	q[10] --> 
// 	q[11] --> 
// 	q[12] --> 
// 	q[13] --> 
// 	q[14] --> 
// 	q[15] --> 
// 	q[16] --> 
// 	q[17] --> 
// 	q[18] --> 
// 	q[19] --> 
OPENQASM 2.0;
include "qelib1.inc";

qreg q[20];
U(1.20000004768372,2.09999990463257,0.5) q[0];
U(1.5707963267949,-0.5,1.20000004768372) q[3];
U(0.400000005960464,0,0) q[1];
U(0,0,0.400000005960464) q[6];
CX q[1],q[6];
CX q[0],q[1];
CX q[1],q[6];
CX q[0],q[1];
U(3.14159265358979,0,3.14159265358979) q[6];
CX q[1],q[2];
U(3.14159265358979,1.5707963267949,1.5707963267949) q[3];
U(1.20000004768372,-1.5707963267949,1.5707963267949) q[6];
U(0,0,3.14159265358979) q[1];
U(1.5707963267949,0,3.14159265358979) q[0];
U(0,0,1.5707963267949) q[3];
CX q[1],q[6];
U(1.5707963267949,0,3.14159265358979) q[2];
CX q[3],q[2];
U(1.5707963267949,0,3.14159265358979) q[2];
U(0,0,-0.785398163397448) q[3];
U(0,0,-1.5707963267949) q[1];
U(0,0,0.785398163397448) q[0];
