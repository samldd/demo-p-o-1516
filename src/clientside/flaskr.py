from flask import Flask, request, session, g, redirect, url_for, \
     abort, render_template, flash, jsonify, Response
from fetch_frame import FileFetcher
from datetime import datetime

import time


app = Flask(__name__)
fetcher = FileFetcher()
fetcher.initialize()

def gen(filefetcher, oneFrame = False):
    while True:
        frame = str(filefetcher.get_frame())
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
        time.sleep(0.05)

@app.route('/video_feed')
def video_feed():
    response = Response(gen(),mimetype='multipart/x-mixed-replace; boundary=frame')
    response.headers['Last-Modified'] = datetime.now()
    response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0, max-age=0'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '-1'
    return response

@app.route('/')
def index():
    return redirect(url_for('video_feed'))


@app.route('/hello_world')
def hello_world():
    return "hello world"

if __name__ == '__main__':
    app.run(debug=False,threaded=True)
