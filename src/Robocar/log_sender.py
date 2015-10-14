import socket


def send_log_to_computer(message, ADDRESS=('192.168.0.103', 3000)):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(3)
    try:
        s.connect(ADDRESS)
        s.send('log')
        s.recv(32) # Anders kan het zijn dat de SocketServer op de pc teveel ineens ontvangt
        s.send(message)
    except Exception, e:
        print e
        raise Exception(("Couldn't send message to %s on port %i.") % (IP, PORT))

