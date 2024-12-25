import os

import pytest

from ouqu_tp.servicers.ouqu_tp import TranspilerService

qasm = """OPENQASM 3;
include "stdgates.inc";
qubit[2] q;

h q[0];
cx q[0], q[1];
"""

device_topology_json = """{
  "name": "test_device",
  "qubits": [
    {
      "id": 0
    },
    {
      "id": 1
    },
    {
      "id": 2
    },
    {
      "id": 3
    }
  ],
  "couplings": [
    {
      "control": 0,
      "target": 2,
      "fidelity": 0.25
    },
    {
      "control": 0,
      "target": 1,
      "fidelity": 0.25
    },
    {
      "control": 1,
      "target": 0,
      "fidelity": 0.25
    },
    {
      "control": 1,
      "target": 3,
      "fidelity": 0.25
    },
    {
      "control": 2,
      "target": 0,
      "fidelity": 0.25
    },
    {
      "control": 2,
      "target": 3,
      "fidelity": 0.25
    },
    {
      "control": 3,
      "target": 1,
      "fidelity": 0.25
    },
    {
      "control": 3,
      "target": 2,
      "fidelity": 0.6000000000000001
    }
  ]
}
"""

device_topology_json_device_id = """{
  "device_id": "test_device",
  "qubits": [
    {
      "id": 0
    },
    {
      "id": 1
    },
    {
      "id": 2
    },
    {
      "id": 3
    }
  ],
  "couplings": [
    {
      "control": 0,
      "target": 2,
      "fidelity": 0.25
    },
    {
      "control": 0,
      "target": 1,
      "fidelity": 0.25
    },
    {
      "control": 1,
      "target": 0,
      "fidelity": 0.25
    },
    {
      "control": 1,
      "target": 3,
      "fidelity": 0.25
    },
    {
      "control": 2,
      "target": 0,
      "fidelity": 0.25
    },
    {
      "control": 2,
      "target": 3,
      "fidelity": 0.25
    },
    {
      "control": 3,
      "target": 1,
      "fidelity": 0.25
    },
    {
      "control": 3,
      "target": 2,
      "fidelity": 0.6000000000000001
    }
  ]
}
"""

expected_qasm = """// Mapped to device "test_device"
// Qubits: 4
// Layout (physical --> virtual):
// \tq[0] --> 
// \tq[1] --> 
// \tq[2] --> q[1]
// \tq[3] --> q[0]
OPENQASM 3.0;
include "stdgates.inc";
qreg q[4];
creg c[4];
rz(1.5707963267948932) q[3];
sx q[3];
rz(1.5707963267948966) q[3];
cx q[3],q[2];
c[3] = measure q[3];
c[2] = measure q[2];

"""


class TestTranspilerService:
    @pytest.mark.skipif(
      os.getenv("GITHUB_ACTIONS") == "true", 
      reason="Skipping this test on GitHub Actions"
    )
    def test_transpile(self) -> None:
        transpiler = TranspilerService()
        response = transpiler.transpile(qasm, device_topology_json)
        assert response.status == "SUCCESS"
        assert response.message == ""
        assert response.qasm == expected_qasm
        assert response.qubit_mapping == {2: 1, 3: 0}  # physical-virtual mapping

    @pytest.mark.skipif(
      os.getenv("GITHUB_ACTIONS") == "true", 
      reason="Skipping this test on GitHub Actions"
    )
    def test_transpile_device_id(self) -> None:
        transpiler = TranspilerService()
        response = transpiler.transpile(qasm, device_topology_json_device_id)
        assert response.status == "SUCCESS"
        assert response.message == ""
        assert response.qasm == expected_qasm
        assert response.qubit_mapping == {2: 1, 3: 0}  # physical-virtual mapping
