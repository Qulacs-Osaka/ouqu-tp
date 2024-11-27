from dataclasses import dataclass
from logging import getLogger
from typing import Any, Dict, Optional

from ouqu_tp.servicers.default_device_topology_json import (
    DEFAULT_DEVICE_TOPOLOGY_JSON,
)
from ouqu_tp.servicers.exec_ouqu import ouqu


@dataclass
class TranspileResponse:
    status: str
    message: str
    qasm: str
    qubit_mapping: Dict[int, int]


class TranspilerService(object):
    def transpile(self, qasm: str, device_topology_json: Optional[str] = None) -> Any:
        logger = getLogger(__name__)
        try:
            logger.debug(f"qasm: {qasm}")
            logger.debug(f"device_topology_json: {device_topology_json}")

            cn_json = ""
            # リクエストで渡されたJSONが優先
            if device_topology_json is None:
                cn_json = DEFAULT_DEVICE_TOPOLOGY_JSON
            else:
                cn_json = device_topology_json

            logger.debug(f"ouqu cn_json: {cn_json}")

            result, mapping = ouqu(qasm, cn_json)
            logger.debug(f"ouqu result: {result}")
            logger.debug(f"ouqu mapping: {mapping}")
            return TranspileResponse(
                status="SUCCESS", message="", qasm=result, qubit_mapping=mapping
            )
        except Exception as e:
            logger.exception(e)
            return TranspileResponse(
                status="FAILURE", message=str(e), qasm="", qubit_mapping={}
            )
