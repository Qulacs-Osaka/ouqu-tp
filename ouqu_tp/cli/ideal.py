import subprocess
import typer
from typing import List

from ouqu_tp.internal.getval import getval_do
from ouqu_tp.internal.sampleval import sampleval_do
from ouqu_tp.internal.simulate import simulate_do

app = typer.Typer()


@app.command()
def getval_ideal_call(
        input_qasm_file: str = typer.Option(...), input_openfermion_file: str = typer.Option(...)) -> None:
    cpl_qasm: List[str] = subprocess.check_output(
        ['staq', '-m', '--evaluate-all', input_qasm_file]).decode().splitlines()
    print(getval_do(cpl_qasm, input_openfermion_file))


@app.command()
def sampleval_ideal_call(
        input_qasm_file: str = typer.Option(...), input_openfermion_file: str = typer.Option(...), shots: int = typer.Option(...)) -> None:
    cpl_qasm: List[str] = subprocess.check_output(
        ['staq', '-m', '--evaluate-all', input_qasm_file]).decode().splitlines()
    print(sampleval_do(cpl_qasm, input_openfermion_file, shots))


@app.command()
def simulate_ideal_call(
        input_qasm_file: str = typer.Option(...), shots: int = typer.Option(...)) -> None:
    cpl_qasm: List[str] = subprocess.check_output(
        ['staq', '-m', '--evaluate-all', input_qasm_file]).decode().splitlines()
    print(simulate_do(cpl_qasm, shots))


if __name__ == "__main__":
    app()
