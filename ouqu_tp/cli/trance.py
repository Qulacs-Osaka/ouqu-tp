import subprocess
from typing import List

import typer

from ouqu_tp.internal.make_Cnet import make_Cnet_put
from ouqu_tp.internal.ot_io import output_gates_QASMfuu, str_to_gate
from ouqu_tp.internal.tran import tran_ouqu_multi

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

    (n_qubit, input_list) = str_to_gate(cpl_qasm, "put")
    tran_gates = tran_ouqu_multi(n_qubit, input_list)
    output_gates_QASMfuu(tran_gates)


@app.command("makeCnet")
def makeCnet_call(
    cnot_net_file: str = typer.Option(...),
) -> None:

    ff = open(cnot_net_file, "r")
    Cnet_list = ff.readlines()
    make_Cnet_put(Cnet_list)


if __name__ == "__main__":
    app()
