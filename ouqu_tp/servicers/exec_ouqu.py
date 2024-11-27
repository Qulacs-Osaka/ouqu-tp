import os
import re
import subprocess
import tempfile
from typing import Dict, Tuple

from parse import parse

from ouqu_tp.servicers import config

DELETE_FLG = config.get_config_DELETE_TMP_FLG()
ADD_INC_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "add.inc")


def add_gate_def(qasm_str: str) -> str:
    result = ""

    def read_add() -> str:
        with open(ADD_INC_PATH) as f:
            s = f.read()
            return s

    for line in qasm_str.split("\n"):
        result = result + line + "\n"
        if "qelib1.inc" in line.lower():
            result = result + read_add() + "\n"

    return result


def convert_qubit_to_qreg(qasm: str) -> str:
    result = ""
    q_str = "q"
    c_str = "c"
    n_size = ""
    is_exist_bit = False
    for line in qasm.split("\n"):
        # 前スペースを取る
        line = line.strip()
        # qubit -> qreg
        ary = parse("qubit[{n}] {v};", line)
        if ary is not None:
            n = ary["n"]
            n_size = n
            v = ary["v"].strip()
            q_str = v
            q = f"qreg {v}[{n}];"
            result = result + q + "\n"
        else:
            # bit -> creg
            ary = parse("bit[{n}] {v};", line)
            if ary is not None:
                is_exist_bit = True
                n = ary["n"]
                n_size = n
                v = ary["v"].strip()
                c_str = v
                q = f"creg {v}[{n}];"
                result = result + q + "\n"
            else:
                result = result + line + "\n"

        # cregが存在する場合
        ary = parse("creg {v}[{n}];", line)
        if ary is not None:
            is_exist_bit = True

    if not is_exist_bit:
        result = result + f"creg c[{n_size}];"

    if "measure" in qasm.lower():
        return result
    else:
        str = result + f"measure {q_str} -> {c_str};"
        return str


def convert_v3_to_v2_measure(qasm: str) -> str:
    result = ""
    for line in qasm.split("\n"):
        # `c = measure q;` -> `measure q -> c;`
        ary = parse("{vc}= measure {vq};", line)
        if ary is not None and ary["vc"][0:2] != "//":
            vc = ary["vc"].strip()
            vq = ary["vq"].strip()
            q = f"measure {vq}->{vc};"
            result = result + q + "\n"
        else:
            result = result + line + "\n"

    return result


def convert_v3_to_v2(qasm: str) -> str:
    str = re.sub(r"OPENQASM\s+3.0;", "OPENQASM 2.0;", qasm, flags=re.IGNORECASE)
    str = re.sub(r"OPENQASM\s+3;", "OPENQASM 2.0;", str, flags=re.IGNORECASE)
    if "stdgates.inc" not in qasm:
        str = re.sub(
            "OPENQASM 2.0;",
            'OPENQASM 2.0;\ninclude "stdgates.inc";\n',
            str,
            flags=re.IGNORECASE,
        )
    str = re.sub("stdgates.inc", "qelib1.inc", str, flags=re.IGNORECASE)

    str = convert_qubit_to_qreg(str)
    str = convert_v3_to_v2_measure(str)
    return str


def convert_v2_to_v3_measure(qasm: str) -> str:
    result = ""
    for line in qasm.split("\n"):
        # `measure q -> c;` -> `c = measure q;`
        ary = parse("measure{vq}->{vc};", line)
        if ary is not None:
            vc = ary["vc"].strip()
            vq = ary["vq"].strip()
            q = f"{vc} = measure {vq};"
            result = result + q + "\n"
        else:
            result = result + line + "\n"

    return result


def convert_v2_to_v3(qasm: str) -> str:
    str = re.sub("OPENQASM 2.0;", "OPENQASM 3.0;", qasm, flags=re.IGNORECASE)
    str = re.sub("qelib1.inc", "stdgates.inc", str, flags=re.IGNORECASE)
    str = convert_v2_to_v3_measure(str)
    return str


def add_newline_to_semicolons(qasm_str: str) -> str:
    # 正規表現でセミコロンに続く改行がない場合に改行を追加する
    pattern = r";(?!\n)"
    repl = ";\n"
    result = re.sub(pattern, repl, qasm_str)
    return result


def exec_ouqu(qasm_str: str, device_topology_json: str) -> str:
    with tempfile.NamedTemporaryFile(mode="w+t", delete=DELETE_FLG) as fcnot:
        fcnot.write(device_topology_json)
        fcnot.seek(0)

        with tempfile.NamedTemporaryFile(mode="w+t", delete=DELETE_FLG) as fqasm:
            fqasm.write(qasm_str)
            fqasm.seek(0)

            cmd = f"ouqu-tp trance trance --input-qasm-file={fqasm.name} --input-cnot-json-file={fcnot.name}"
            subprocess_output = subprocess.run(
                cmd, capture_output=True, text=True, shell=True
            )
            # TODO:swapでなぜか、staqが"Error: linear operator is not invertible"を標準エラーに出力するので対応
            if len(subprocess_output.stderr) > 0:
                if (
                    "Error: linear operator is not invertible"
                    in subprocess_output.stderr
                ):
                    return subprocess_output.stdout
                else:
                    raise Exception(subprocess_output.stderr)
            return subprocess_output.stdout


def get_mapping(qasm: str) -> Dict[int, int]:
    mapping = {}

    for line in qasm.split("\n"):
        instr = line.lower().strip().replace(" ", "").replace("\t", "")
        if instr[0:4] == "//q[":
            ary = parse("//q[{:d}]-->q[{:d}]", instr)
            if ary is not None:
                mapping[ary[0]] = ary[1]

    return mapping


def ouqu(qasm_str: str, device_topology_json: str) -> Tuple[str, Dict[int, int]]:
    qasm_str = add_newline_to_semicolons(qasm_str)
    qasm_str = convert_v3_to_v2(qasm_str)
    qasm_str = add_gate_def(qasm_str)
    result = exec_ouqu(qasm_str, device_topology_json)
    result = convert_v2_to_v3(result)
    mapping = get_mapping(result)
    return result, mapping
