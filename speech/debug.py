from os.path import isdir

def is_debug_mode():
    if isdir('.git'):
        return True
    return False
