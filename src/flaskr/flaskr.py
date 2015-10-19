from flask import Flask, request, session, g, redirect, url_for, \
     abort, render_template, flash

import interface

app = Flask(__name__)

@app.route('/', methods=['POST', 'GET'])
def show_entries():
    if request.method == 'POST':
        if request.form['submit'] == 'forward':
            interface.forward()
        elif request.form['submit'] == 'backward':
            interface.backward()
        elif request.form['submit'] == 'left':
            interface.left()
        elif request.form['submit'] == 'right':
            interface.right()
    return render_template('index.html')

if __name__ == '__main__':
    app.run()
