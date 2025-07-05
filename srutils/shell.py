import logging
import os
import subprocess

logger = logging.getLogger("py-commons")

def _cmd(cmd):
    """Helper function to format a command for execution."""
    if isinstance(cmd, str):
        return cmd
    elif isinstance(cmd, list):
        return " ".join(cmd)
    else:
        return str(cmd)

def shell_system(cmd):
    cmd = _cmd(cmd)
    logger.debug(f"shell_system: {cmd}")
    os.system(cmd)

def shell_popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE):
    """
    Execute a shell command using subprocess.Popen.
    stdout can be a file.
    """
    cmd = _cmd(cmd)
    logger.debug(f"shell_popen: {cmd}")
    proc = subprocess.Popen(
        f"exec {cmd}",
        cwd=os.getcwd(),
        shell=True,
        stdout=stdout,
        stderr=subprocess.STDOUT,
        stdin=stdin,
        universal_newlines=True,
        env=os.environ,
    )
    return proc