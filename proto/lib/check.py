from asyncio import subprocess
import subprocess


def check_node() -> bool:
    """
    Check if node is installed on the system.

    :return: true if Node is installed on the system.
    """
    try:
        subprocess.check_output("node -v", shell=True)
        return True
    except subprocess.CalledProcessError:
        return False


def check_go() -> bool:
    """
    Check if Go is installed on the system.

    :return: true if Go is installed on the system.
    """
    try:
        subprocess.check_output("go version", shell=True)
        return True
    except subprocess.CalledProcessError:
        return False
