from flask import Flask, request, session, g, redirect, url_for, \
     abort, render_template, flash, jsonify, Response
#import socket_client
import interface, sys, traceback

##voor stream
#from camera import Camera

app = Flask(__name__)

@app.route('/acc')
def receive_accelerometer_data():
    xValue = int(request.args.get('xValue'))
    yValue = int(request.args.get('yValue'))
    interface.drive_accelerometer(xValue, yValue)
    return "send your accelerometer data here"

@app.route('/info')
def show_pi_information():
    return render_template('information.html', info=interface.get_debug_info())



def gen(camera):
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(gen(Camera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/', methods=['POST', 'GET'])
def show_index():
    #if socket_client.s == None:
        #socket_client.startSocket(request.remote_addr)

    if request.method == 'POST':
        return_sentence = 'executed command ' + request.form['submit']
        try:
            if request.form['submit'] == 'forward':
                interface.forward()
            elif request.form['submit'] == 'backward':
                interface.backward()
            elif request.form['submit'] == 'left':
                interface.left()
            elif request.form['submit'] == 'right':
                interface.right()
            elif request.form['submit'] == 'sharpleft':
                interface.sharpleft()
            elif request.form['submit'] == 'sharpright':
                interface.sharpright()
            elif request.form['submit'] == 'line':
                interface.line()
            elif request.form['submit'] == 'square':
                interface.square()
            elif request.form['submit'] == 'circle':
                interface.circle()
            elif request.form['submit'] == 'kill':
                interface.kill()
            elif request.form['submit'] == 'picture':
                interface.picture()
            elif request.form['submit'] == 'stream':
                interface.stream()
            elif request.form['submit'] == 'followline':
                interface.followline()
            elif request.form['submit'] == 'stopdriving':
                interface.forward(0)
            else:
                return render_template('debug_sentence.html', sentence='unknown command received')
        except:
            return_sentence = traceback.format_exc().replace('\n', '<br />')
        return render_template('debug_sentence.html', sentence=return_sentence)
    else:
        return render_template('index.html')

if __name__ == '__main__':
    if sys.platform == 'win32':
        app.run()
    else:
        app.run(host='0.0.0.0')