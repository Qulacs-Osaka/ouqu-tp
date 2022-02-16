import subprocess
from typing import List

import typer

from ouqu_tp.internal.getval import getval_noise_do
from ouqu_tp.internal.sampleval import sampleval_noise_do
from ouqu_tp.internal.simulate import simulate_noise_do

app = typer.Typer()


@app.command("getval")
def getval_noisy_call(
    input_qasm_file: str = typer.Option(...),
    input_openfermion_file: str = typer.Option(...),
    p1: float = 0,
    p2: float = 0,
    pm: float = 0,
    pp: float = 0,
) -> None:
    cpl_qasm: List[str] = (
        subprocess.check_output(["staq", "-m", "--evaluate-all", input_qasm_file])
        .decode()
        .splitlines()
    )
    print(getval_noise_do(cpl_qasm, input_openfermion_file, p1, p2, pm, pp))


@app.command("sampleval")
def sampleval_noisy_call(
    input_qasm_file: str = typer.Option(...),
    input_openfermion_file: str = typer.Option(...),
    shots: int = typer.Option(...),
    p1: float = 0,
    p2: float = 0,
    pm: float = 0,
    pp: float = 0,
) -> None:
    cpl_qasm: List[str] = (
        subprocess.check_output(["staq", "-m", "--evaluate-all", input_qasm_file])
        .decode()
        .splitlines()
    )
    print(sampleval_noise_do(cpl_qasm, input_openfermion_file, shots, p1, p2, pm, pp))


@app.command("simulate")
def simulate_noisy_call(
    input_qasm_file: str = typer.Option(...),
    shots: int = typer.Option(...),
    p1: float = 0,
    p2: float = 0,
    pm: float = 0,
    pp: float = 0,
) -> None:
    cpl_qasm: List[str] = (
        subprocess.check_output(["staq", "-m", "--evaluate-all", input_qasm_file])
        .decode()
        .splitlines()
    )
    print(simulate_noise_do(cpl_qasm, shots, p1, p2, pm, pp))


if __name__ == "__main__":
    app()
