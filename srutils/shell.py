import logging
import os
import subprocess
import tempfile
import time

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


def shell_get_stdout_retcode(cmd, display_output=False):
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
        if display_output:
            print(output)
    return output, proc.returncode


def shell_check_output_kill(cmd, target_text, terminate_func=None, time_before_kill=1):
    # might be in an infinite loop, if a wrong target_text is given
    cmd = _cmd(cmd)
    logger.debug(f"shell_check_output_kill: {cmd}")
    proc = subprocess.Popen(
        cmd,
        cwd=os.getcwd(),
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        stdin=subprocess.PIPE,
        universal_newlines=True,
        env=os.environ,
    )
    while True:
        line = proc.stdout.readline()
        print(line, end='')
        if target_text in line:
            time.sleep(time_before_kill)
            if terminate_func:
                terminate_func()
            else:
                proc.terminate()
            break
    proc.wait()
