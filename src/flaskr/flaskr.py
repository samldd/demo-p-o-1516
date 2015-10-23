from flask import Flask, request, session, g, redirect, url_for, \
     abort, render_template, flash

import interface

app = Flask(__name__)

@app.route('/info')
def show_pi_information():
    return render_template('information.html', info=interface.get_debug_info())

@app.route('/', methods=['POST', 'GET'])
def show_index():
    if request.method == 'POST':
        if request.form['submit'] == 'forward':
            interface.forward()
            return render_template('debug_sentence.html', sentence='executed command forward')
        elif request.form['submit'] == 'backward':
            interface.backward()
            return render_template('debug_sentence.html', sentence='executed command backward')
        elif request.form['submit'] == 'left':
            interface.left()
            return render_template('debug_sentence.html', sentence='executed command left')
        elif request.form['submit'] == 'right':
            interface.right()
            return render_template('debug_sentence.html', sentence='executed command right')
        elif request.form['submit'] == 'line':
            interface.line()
            return render_template('debug_sentence.html', sentence='executed command line')
        elif request.form['submit'] == 'square':
            interface.square()
            return render_template('debug_sentence.html', sentence='executed command square')
        elif request.form['submit'] == 'circle':
            interface.circle()
            return render_template('debug_sentence.html', sentence='executed command circle')
        elif request.form['submit'] == 'kill':
            interface.kill()
            return render_template('debug_sentence.html', sentence='executed command kill')
        else:
            return render_template('debug_sentence.html', sentence='unknown command received')
    else:
        return render_template('index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0')
