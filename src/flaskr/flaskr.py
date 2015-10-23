from flask import Flask, request, session, g, redirect, url_for, \
     abort, render_template, flash

import interface, sys, traceback

app = Flask(__name__)

@app.route('/info')
def show_pi_information():
    return render_template('information.html', info=interface.get_debug_info())

@app.route('/', methods=['POST', 'GET'])
def show_index():
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