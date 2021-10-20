OPENQASM 2.0;
include "qelib1.inc";

//ありとあらゆるゲートを試す

qreg q[5];
u3(1.2,2.1,0.5) q[0];
u2(-0.5,1.2) q[1];
ry(0.4) q[4];
u1(0.4) q[2];
cx q[0],q[2];
id q[3];
x q[2];
cx q[4],q[3];
y q[1];
rx(1.2) q[2];
z q[4];
h q[0];
cx q[4],q[2];
s q[1];
cz q[1],q[3];
sdg q[4];
t q[0];
tdg q[1];
cx q[0],q[1];
cx q[0],q[1];
