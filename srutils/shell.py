import logging
import os
import subprocess
import tempfile

logger = logging.getLogger("srutils")


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
        cmd,
        cwd=os.getcwd(),
        shell=True,
        stdout=stdout,
        stderr=subprocess.STDOUT,
        stdin=stdin,
        universal_newlines=True,
        env=os.environ,
    )
    return proc


def shell_get_stdout_retcode(cmd):
    """
    Execute a shell command and return its output and return code for short running commands.
    """
    cmd = _cmd(cmd)
    logger.debug(f"shell_get_output: {cmd}")
    with tempfile.TemporaryFile(mode='w+') as temp_file:
        proc = subprocess.Popen(
            cmd,
            cwd=os.getcwd(),
            shell=True,
            stdout=temp_file,
            stderr=subprocess.STDOUT,
            stdin=subprocess.PIPE,
            universal_newlines=True,
            env=os.environ,
        )
        proc.wait()
        temp_file.seek(0)
        output = temp_file.read()
    return output, proc.returncode
