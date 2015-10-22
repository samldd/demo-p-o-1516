import subprocess
from time import gmtime, strftime

def debug(f):            # debug decorator takes function f as parameter
    msg = f.__name__     # debug message to print later
    def wrapper(*args):  # wrapper function takes function f's parameters
        print msg        # print debug message
        return f(*args)  # call to original function
    return wrapper       # return the wrapper function, without calling it

@debug
def forward():
    pass

@debug
def backward():
    pass

@debug
def left():
    pass

@debug
def right():
    pass

@debug
def kill():
    ##windows
    #subprocess.call(["Taskkill", "/F", "/IM", "python.exe"])
    subprocess.call(["killall" "python"])

@debug
def get_debug_info():
    return "it is now: %s"%strftime("%d/%m/%Y %H:%M:%S", gmtime())