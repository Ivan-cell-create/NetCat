import subprocess
import shlex

def execute(cmd):
    cmd = cmd.strip()
    if not cmd:
        return ''
    try:
        output = subprocess.check_output(shlex.split(cmd),
                                         stderr=subprocess.STDOUT)
        return output.decode()
    except subprocess.CalledProcessError as e:
        return e.output.decode()