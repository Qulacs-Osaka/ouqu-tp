import subprocess
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
    out_QASM = trance_do(cpl_qasm)
    for aaa in cpl_qasm:
        if aaa[0:2]=="//":
            print(aaa)
            #コメントの垂れ流しを行います
    for aaa in out_QASM:
        print(aaa)


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
    out_QASM = trance_res_do(cpl_qasm)
    for aaa in cpl_qasm:
        if aaa[0:2]=="//":
            print(aaa)
            #コメントの垂れ流しを行います
    for aaa in out_QASM:
        print(aaa)


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
    ff = open(cnot_net_file, "r")
    Cnet_list = ff.readlines()
    result_array = trance_pulse_do(cpl_qasm, Cnet_list, dt, OZ, OX, ORes, 0)
    np.set_printoptions(threshold=99999999)
    for aaa in cpl_qasm:
        if aaa[0:2]=="//":
            print(aaa)
            #コメントの垂れ流しを行います
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
