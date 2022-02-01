# used to style bash output
class BASHColors:
    FAIL = '\033[91m'
    OKGREEN = '\033[92m'
    ENDC = '\033[0m'


def is_float(word):
    temp = False
    try:
        float(word)
        temp = True
    except:
        temp = False
    return temp
