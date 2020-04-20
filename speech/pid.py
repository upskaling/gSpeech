import os
from os.path import isfile

def kill_if_already_exist(app_name, pid_path):
    '''is PID exists ? If right, try to kill it.'''
    if isfile(pid_path):
        with open(pid_path, 'r') as f:
            pid = int(f.read())
        try:
            os.kill(pid, 0)
        except OSError:
            pass
        else:
            print(
                "** %s is already running\nOtherwise, delete %s" %\
                (app_name, pid_path)
            )
            quit()

    pid = "%s" % os.getpid()
    with open(pid_path, 'w') as f:
        f.write(pid)

def remove(pid):
    '''remove file with current process pid'''
    if isfile(pid):
        os.remove(pid)
