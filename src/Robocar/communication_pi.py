import SocketServer 
import sys 
import cPickle

##################################################
## LISTEN TO INFORMATION COMING FROM A COMPUTER ##
##################################################
class service(SocketServer.BaseRequestHandler):

    def handle(self):
        (ip, _) = self.client_address
        print "Client connected with ", ip

        data = self.request.recv(16)
        print "Data received: %s" % data
        methods = {
            "start": self.start_car,
            "stop": self.stop_car,
            "image": self.send_image, 
            "shutdown": self.shutdown_all,
            "drive": self.drive_car,
            "turn": self.turn_car,
            "": self.set_ip,
        }

        try:
            methods[data]()
        except Exception, e:
            print e
            
    def start_car(self):
        self.request.send('ok')
        instructions = self.request.recv(1024)
        robocar.start_threads()
        AI.execute_instructions(cPickle.loads(instructions))

    def stop_car(self):
        AI.drive_straight(0)
        robocar.stop_threads()
    
    def send_image(self):
        robocar.get_picture()

    def shutdown_all(self):
        robocar.stop_threads()
        shutdown_server()

    def drive_car(self):
        self.request.send('k')
        distance = float(self.request.recv(32))
        AI.drive_straight(distance)

    def turn_car(self):
        self.request.send('k')
        degrees = float(self.request.recv(32))
        AI.turn(degrees)

    def set_ip(self):
        (ip, _) = self.client_address
        robocar.update_ip(ip)
    
class ThreadedTCPServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
    pass

"""
Creating socket server on PI
    Port: 1500
    IP-adress: localhost (=192.168.42.1)
"""
def activate_server(car=None, ai=None):
    
    if not car:
        raise ValueError("robocar not initialized")
    if not ai:
        raise ValueError("AI not initialized")
    
    global robocar, AI
    robocar = car
    AI = ai
    try:
        print "============================"
        print "== Listening on port %i ==" % PORT
        print "============================"
        server.serve_forever()
    except:
        sys.exit("Couldn't serve forever anymore")

def shutdown_server():
    print "Server on pi has been shut down"
    server.shutdown()

robocar = None
AI = None
PORT = 1500
server = ThreadedTCPServer(('', PORT), service)
