from flask import Flask, request, session, g, redirect, url_for, \
     abort, render_template, flash, jsonify, Response
import interface, sys, traceback
import time

if sys.platform != 'win32':
    ##voor stream
    from camera import Camera
    cam = Camera()

app = Flask(__name__)

@app.route('/acc')
def receive_accelerometer_data():
    xValue = int(request.args.get('xValue'))
    yValue = int(request.args.get('yValue'))
    interface.drive_accelerometer(xValue, yValue)
    return "send your accelerometer data here"

@app.route('/line_info')
def receive_line_following_info():
    x = request.args.get('x')
    interface.follow_line(x)
    return "send your line data here"

@app.route('/info')
def show_pi_information():
    return render_template('information.html', info=interface.get_debug_info())

@app.route('/show_action_queue')
def show_command_queue():
    return render_template('showactionqueue.html', command_queue=interface.commandQueue)



def gen(camera, oneFrame = False):
    while True:
        frame = camera.get_frame()
        #frame = photo_recognition.detect_lines(a)
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
        time.sleep(0.15)

@app.route('/hello_world')
def hello_world():
    return "hello world"

@app.route('/video_feed')
def video_feed():
    return Response(gen(cam),mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/video_frame.jpg')
def get_video_frame():
    frame = cam.get_frame()
    return Response(frame, mimetype='image/jpeg')


@app.route('/man')
def receive_manual_commands():
    command = request.args.get('command')
    if command == 'forward':
        interface.forward()
    elif command == 'backward':
        interface.backward()
    elif command == 'left':
        interface.left()
    elif command == 'right':
        interface.right()
    elif command == 'stopdriving':
        interface.brake()
    return "send manual driving instructions via get here"

@app.route('/accelerometer', methods=['POST', 'GET'])
def show_accelerometer_page():
    if request.method == 'POST':
        if request.form['submit'] == 'forward':
            interface.forward()
        elif request.form['submit'] == 'backward':
            interface.backward()
        elif request.form['submit'] == 'left':
            interface.left()
        elif request.form['submit'] == 'right':
            interface.right()
        elif request.form['submit'] == 'stopdriving':
            interface.brake()
        return "should be invisible"
    else:
        return render_template('accelerometer.html')

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
            elif request.form['submit'] == 'kill':
                interface.kill()
            elif request.form['submit'] == 'picture':
                interface.picture()
            elif request.form['submit'] == 'stream':
                interface.stream()
            elif request.form['submit'] == 'followline':
                interface.drive_auto()
            elif request.form['submit'] == 'manual':
                interface.manual()
            elif request.form['submit'] == 'stopdriving':
                interface.brake()
            elif request.form['submit'] == 'nextleft':
                interface.addCommand("left")
            elif request.form['submit'] == 'nextforward':
                interface.addCommand("forward")
            elif request.form['submit'] == 'nextright':
                interface.addCommand("right")
            else:
                return render_template('debug_sentence.html', sentence='unknown command received')
        except:
            return_sentence = traceback.format_exc().replace('\n', '<br />')
        return render_template('debug_sentence.html', sentence=return_sentence)
    else:
        return render_template('index.html')

if __name__ == '__main__':
    if sys.platform == 'win32':
        app.run(debug=True,threaded=True)
    else:
        app.run(host='0.0.0.0', debug=False,threaded=True)