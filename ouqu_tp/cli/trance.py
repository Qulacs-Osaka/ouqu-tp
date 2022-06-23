import subprocess
import sys
from typing import List

import numpy as np
import typer

from ouqu_tp.internal.make_Cnet import make_Cnet_put
from ouqu_tp.internal.trancepile import (
    trance_do,
    trance_pulse_do,
    trance_res_do,
)

app = typer.Typer()


@app.command("trance")
def trance_call(
    input_qasm_file: str = typer.Option(...),
    input_cnot_json_file: str = typer.Option(...),
    direct_qasm: bool = False,
) -> None:
    cpl_qasm: List[str]
    if direct_qasm:
        cpl_qasm = open(input_qasm_file, "r").readlines()
    else:
        cpl_qasm = (
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
    out_QASM = trance_do(cpl_qasm)
    for cpl_qasm_comment_line in cpl_qasm:
        if cpl_qasm_comment_line[0:2] == "//":
            print(cpl_qasm_comment_line)
            # コメントの垂れ流しを行います
    for QASM_line in out_QASM:
        print(QASM_line)


@app.command("trance_res")
def trance_res_call(
    input_qasm_file: str = typer.Option(...),
    input_cnot_json_file: str = typer.Option(...),
    direct_qasm: bool = False,
) -> None:
    cpl_qasm: List[str]
    if direct_qasm:
        cpl_qasm = open(input_qasm_file, "r").readlines()
    else:
        cpl_qasm = (
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
    out_QASM = trance_res_do(cpl_qasm)
    for cpl_qasm_comment_line in cpl_qasm:
        if cpl_qasm_comment_line[0:2] == "//":
            print(cpl_qasm_comment_line)
            # コメントの垂れ流しを行います
    for QASM_line in out_QASM:
        print(QASM_line)


@app.command("trance_pulse")
def trance_pulse_call(
    input_qasm_file: str = typer.Option(...),
    input_cnot_json_file: str = typer.Option(...),
    cnot_net_file: str = typer.Option(...),
    dt: float = 0.01,
    OZ: float = 10,
    OX: float = 10,
    ORes: float = 1,
    direct_qasm: bool = False,
) -> None:
    cpl_qasm: List[str]
    if direct_qasm:
        cpl_qasm = open(input_qasm_file, "r").readlines()
    else:
        cpl_qasm = (
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
    ff = open(cnot_net_file, "r")
    Cnet_list = ff.readlines()
    result_array = trance_pulse_do(cpl_qasm, Cnet_list, dt, OZ, OX, ORes, 0)
    np.set_printoptions(threshold=99999999)
    """
    for cpl_qasm_comment_line in cpl_qasm:
        if cpl_qasm_comment_line[0:2] == "//":
            print(cpl_qasm_comment_line)
            # コメントの垂れ流しを行います
    """
    np.savetxt(sys.stdout.buffer, result_array)
    # savetxt で出力したかったからこうなった


@app.command("makeCnet")
def makeCnet_call(
    cnot_net_file: str = typer.Option(...),
) -> None:

    ff = open(cnot_net_file, "r")
    Cnet_list = ff.readlines()
    make_Cnet_put(Cnet_list)


if __name__ == "__main__":
    app()
