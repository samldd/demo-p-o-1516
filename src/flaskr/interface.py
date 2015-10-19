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