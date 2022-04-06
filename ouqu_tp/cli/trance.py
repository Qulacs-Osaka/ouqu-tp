import re
import subprocess
from typing import List

import typer

from ouqu_tp.internal.make_Cnet import make_Cnet_put,get_connect
from ouqu_tp.internal.ot_io import output_gates_QASMfuu, str_to_gate
from ouqu_tp.internal.tran import CNOT_to_CRes, tran_ouqu_multi, tran_to_pulse

app = typer.Typer()


@app.command("trance")
def trance_call(
    input_qasm_file: str = typer.Option(...),
    input_cnot_json_file: str = typer.Option(...),
) -> None:
    cpl_qasm: List[str] = (
        subprocess.check_output(
            [
                "staq",
                "-S",
                "-O2",
                "-m",
                "-d",
                input_cnot_json_file,
                "--evaluate-all",
                input_qasm_file,
            ]
        )
        .decode()
        .splitlines()
    )

    (n_qubit, input_list) = str_to_gate(cpl_qasm, "put", False)
    tran_gates = tran_ouqu_multi(n_qubit, input_list)
    output_gates_QASMfuu(tran_gates)


@app.command("trance_res")
def trance_res_call(
    input_qasm_file: str = typer.Option(...),
    input_cnot_json_file: str = typer.Option(...),
) -> None:
    cpl_qasm: List[str] = (
        subprocess.check_output(
            [
                "staq",
                "-S",
                "-O2",
                "-m",
                "-d",
                input_cnot_json_file,
                "--evaluate-all",
                input_qasm_file,
            ]
        )
        .decode()
        .splitlines()
    )

    (n_qubit, input_list) = str_to_gate(cpl_qasm, "put", False)
    tran_gates = tran_ouqu_multi(n_qubit, CNOT_to_CRes(input_list))
    output_gates_QASMfuu(tran_gates)


@app.command("trance_pulse")
def trance_pulse_call(
    input_qasm_file: str = typer.Option(...),
    input_cnot_json_file: str = typer.Option(...),
    cnot_net_file: str = typer.Option(...),
    dt: float = 0.01,
    OZ: float = 10,
    OX: float = 10,
    ORes: float = 1,
) -> None:
    cpl_qasm: List[str] = (
        subprocess.check_output(
            [
                "staq",
                "-S",
                "-O2",
                "-m",
                "-d",
                input_cnot_json_file,
                "--evaluate-all",
                input_qasm_file,
            ]
        )
        .decode()
        .splitlines()
    )
    (n_qubit, input_list) = str_to_gate(cpl_qasm, "put", False)
    ff = open(cnot_net_file, "r")
    Cnet_list = ff.readlines()
    can_gate = get_connect(Cnet_list)
    result_array = tran_to_pulse(
        n_qubit, input_list, can_gate, dt * OZ, dt * OX, dt * ORes, 0
    )
    print(result_array)


@app.command("makeCnet")
def makeCnet_call(
    cnot_net_file: str = typer.Option(...),
) -> None:

    ff = open(cnot_net_file, "r")
    Cnet_list = ff.readlines()
    make_Cnet_put(Cnet_list)


if __name__ == "__main__":
    app()
