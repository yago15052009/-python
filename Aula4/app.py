from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/python')
def page1():
    return render_template('page1.html')

@app.route('/flask')
def page2():
    return render_template('page2.html')

@app.route('/estudante')
def page3():
    return render_template('page3.html')

if __name__ == '__main__':
    app.run(debug=True)
