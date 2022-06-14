import subprocess
from typing import List

import typer

from ouqu_tp.internal.getval import getval_do
from ouqu_tp.internal.sampleval import sampleval_do
from ouqu_tp.internal.simulate import simulate_do

app = typer.Typer()


@app.command("getval")
def getval_ideal_call(
    input_qasm_file: str = typer.Option(...),
    input_openfermion_file: str = typer.Option(...),
    direct_qasm: bool = False,
) -> None:
    cpl_qasm: List[str]
    if direct_qasm:
        cpl_qasm = open(input_qasm_file, "r").readlines()
    else:
        cpl_qasm = (
            subprocess.check_output(["staq", "-m", "--evaluate-all", input_qasm_file])
            .decode()
            .splitlines()
        )
    print(getval_do(cpl_qasm, input_openfermion_file))


@app.command("sampleval")
def sampleval_ideal_call(
    input_qasm_file: str = typer.Option(...),
    input_openfermion_file: str = typer.Option(...),
    shots: int = typer.Option(...),
    direct_qasm: bool = False,
) -> None:
    cpl_qasm: List[str]
    if direct_qasm:
        cpl_qasm = open(input_qasm_file, "r").readlines()
    else:
        cpl_qasm = (
            subprocess.check_output(["staq", "-m", "--evaluate-all", input_qasm_file])
            .decode()
            .splitlines()
        )
    print(sampleval_do(cpl_qasm, input_openfermion_file, shots))


@app.command("simulate")
def simulate_ideal_call(
    input_qasm_file: str = typer.Option(...),
    shots: int = typer.Option(...),
    direct_qasm: bool = False,
) -> None:
    cpl_qasm: List[str]
    if direct_qasm:
        cpl_qasm = open(input_qasm_file, "r").readlines()
    else:
        cpl_qasm = (
            subprocess.check_output(["staq", "-m", "--evaluate-all", input_qasm_file])
            .decode()
            .splitlines()
        )
    (kekka, n_qubit) = simulate_do(cpl_qasm, shots)
    # input_listを直接ぶち込む
    for aaaa in kekka:
        moziretu = "{:b}".format(aaaa)
        while len(moziretu) < n_qubit:
            moziretu = "0" + moziretu
        print(moziretu)


if __name__ == "__main__":
    app()
