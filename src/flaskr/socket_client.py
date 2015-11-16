import socket               # Import socket module

s = None
def startSocket(hostIp):
    global s
    s = socket.socket()         # Create a socket object
    host = hostIp
    port = 12345                # Reserve a port for your service.

    s.connect((host, port))

def sendImage():
    f = open('static/last_image.img','rb')
    print 'Sending...'
    l = f.read(1024)
    while l:
        print 'Sending...'
        s.send(l)
        l = f.read(1024)
    f.close()
    print "Done Sending"
    s.shutdown(socket.SHUT_WR)
    print s.recv(1024) #dit is resultaat van de functie die opgeroepen werd

def stopStocket():
    s.close()