import logging
import subprocess
import os
from xmlrpc.client import Boolean

import typer

import ouqu_tp.cli.ideal as ideal
import ouqu_tp.cli.noisy as noisy
import ouqu_tp.cli.trance as trance

app = typer.Typer()
app.add_typer(ideal.app, name="ideal")
app.add_typer(noisy.app, name="noisy")
app.add_typer(trance.app, name="trance")

def is_staq_installed() -> bool:
    """
    Check if 'staq' is installed and accessible via the command line.
    """
    try:
        subprocess.run(
            ["staq", "--help"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            check=True,
        )
        return True
    except (FileNotFoundError, subprocess.CalledProcessError):
        return False

def install_staq() -> None:
    """
    Clone, build, and install the 'staq' tool from its GitHub repository.
    """
    repo_url = "https://github.com/softwareQinc/staq.git"
    base_dir = os.path.dirname(os.path.abspath(__file__))
    staq_dir = os.path.join(base_dir, "..", "external", "staq")

    if not os.path.exists(staq_dir):
        try:
            subprocess.check_call(["git", "clone", repo_url, staq_dir], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        except subprocess.CalledProcessError:
            return

    staq_build_dir = os.path.join(staq_dir, "build")
    os.makedirs(staq_build_dir, exist_ok=True)

    try:
        subprocess.check_call(["cmake", staq_dir], cwd=staq_build_dir, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        subprocess.check_call(["make"], cwd=staq_build_dir, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        subprocess.check_call(["sudo", "make", "install"], cwd=staq_build_dir, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except subprocess.CalledProcessError:
        return

def main():
    if not is_staq_installed():
        install_staq()

    app()

if __name__ == "__main__":
    main()
