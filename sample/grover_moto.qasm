OPENQASM 2.0;
include "qelib1.inc";
gate gate_U___omega_ q0,q1,q2 { cz q0,q2; cz q1,q2; }
gate gate_U__s_ q0,q1,q2 { h q0; h q1; h q2; x q0; x q1; x q2; h q2; ccx q0,q1,q2; h q2; x q0; x q1; x q2; h q0; h q1; h q2; }
qreg q[3];
creg meas[3];
h q[0];
h q[1];
h q[2];
gate_U___omega_ q[0],q[1],q[2];
gate_U__s_ q[0],q[1],q[2];
barrier q[0],q[1],q[2];
measure q[0] -> meas[0];
measure q[1] -> meas[1];
measure q[2] -> meas[2];
