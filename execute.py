import subprocess
import shlex
import platform


"""
Метод execute, который определяет ОС юзера 
cmd - строка с командой системы 
"""
def execute(cmd):
    cmd = cmd.strip()
    if not cmd:
        return ''
    try:
        if platform.system().lower() == 'windows':
            output = subprocess.check_output(cmd, stderr=subprocess.STDOUT, shell=True)
        else:
            output = subprocess.check_output(shlex.split(cmd), stderr=subprocess.STDOUT)
        return output.decode()
    except subprocess.CalledProcessError as e:
        return e.output.decode()