import logging
import subprocess
from xmlrpc.client import Boolean

import typer

import ouqu_tp.cli.ideal as ideal
import ouqu_tp.cli.noisy as noisy
import ouqu_tp.cli.trance as trance

app = typer.Typer()
app.add_typer(ideal.app, name="ideal")
app.add_typer(noisy.app, name="noisy")
app.add_typer(trance.app, name="trance")


def is_staq_installed() -> Boolean:
    try:
        subprocess.run(["staq", "--help"], stdout=subprocess.DEVNULL, check=True)
        return True
    except Exception:
        return False


@app.callback()
def debugflag(debug: bool = False) -> None:
    """
    Debug mode for output log files.
    """
    if debug:
        logger = logging.getLogger()
        formatter = logging.Formatter(
            "%(asctime)s %(name)s %(funcName)s [%(levelname)s]: %(message)s"
        )
        handler = logging.StreamHandler()
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.setLevel(logging.DEBUG)


def main() -> None:
    if is_staq_installed() is False:
        raise Exception(
            "[ERROR] staq seems to be not installed.\n"
            "please install staq from https://github.com/softwareQinc/staq"
        )

    app()


if __name__ == "__main__":
    main()
