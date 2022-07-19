import subprocess
from typing import List

import typer

from ouqu_tp.internal.getval import getval_noiseevo_do
from ouqu_tp.internal.sampleval import sampleval_noiseevo_do
from ouqu_tp.internal.simulate import simulate_noiseevo_do

app = typer.Typer()


@app.command("getval")
def getval_noisyevo_call(
    input_qasm_file: str = typer.Option(...),
    input_cnot_json_file: str = typer.Option(...),
    input_openfermion_file: str = typer.Option(...),
    shots: int = typer.Option(...),
    dt: float = 0.01,
    OZ: float = 1.0,
    OX: float = 1.0,
    ORes: float = 1.0,
    decay_rate_ph: float = 0.0,
    decay_rate_amp: float = 0.0,
    evodt: float = 0.5,
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
    print(
        getval_noiseevo_do(
            cpl_qasm,
            input_openfermion_file,
            shots,
            dt,
            OZ,
            OX,
            ORes,
            decay_rate_ph,
            decay_rate_amp,
            evodt,
        )
    )


@app.command("sampleval")
def sampleval_noisyevo_call(
    input_qasm_file: str = typer.Option(...),
    input_cnot_json_file: str = typer.Option(...),
    input_openfermion_file: str = typer.Option(...),
    shots: int = typer.Option(...),
    dt: float = 0.01,
    OZ: float = 1.0,
    OX: float = 1.0,
    ORes: float = 1.0,
    decay_rate_ph: float = 0.0,
    decay_rate_amp: float = 0.0,
    evodt: float = 0.5,
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
    print(
        sampleval_noiseevo_do(
            cpl_qasm,
            input_openfermion_file,
            shots,
            dt,
            OZ,
            OX,
            ORes,
            decay_rate_ph,
            decay_rate_amp,
            evodt,
        )
    )


@app.command("simulate")
def simulate_noisyevo_call(
    input_qasm_file: str = typer.Option(...),
    input_cnot_json_file: str = typer.Option(...),
    shots: int = typer.Option(...),
    dt: float = 0.01,
    OZ: float = 1.0,
    OX: float = 1.0,
    ORes: float = 1.0,
    decay_rate_ph: float = 0.0,
    decay_rate_amp: float = 0.0,
    evodt: float = 0.5,
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
    (kekka, n_qubit) = simulate_noiseevo_do(
        cpl_qasm,
        shots,
        dt,
        OZ,
        OX,
        ORes,
        decay_rate_ph,
        decay_rate_amp,
        evodt,
    )
    # input_listを直接ぶち込む
    for aaaa in kekka:
        moziretu = "{:b}".format(aaaa)
        while len(moziretu) < n_qubit:
            moziretu = "0" + moziretu
        print(moziretu)


if __name__ == "__main__":
    app()
