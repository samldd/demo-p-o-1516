import communication_pi
import threading

import RoboCar as R
import AI as A
 
car = R.RoboCar()
ai = A.AI(car)

threading.Thread(target=communication_pi.activate_server(car, ai)).start()

