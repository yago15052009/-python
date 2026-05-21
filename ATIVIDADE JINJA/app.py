from flask import Flask, render_template

app = Flask(__name__)

# Exercício 1
@app.route("/")
def ex1():
    return render_template("index.html", nome="Maria")

# Exercício 2
@app.route("/ex2")
def ex2():
    return render_template("ex2.html", nome="Carlos", idade=20)

# Exercício 3
@app.route("/ex3")
def ex3():
    usuario = {"nome": "Ana", "email": "ana@email.com"}
    return render_template("ex3.html", usuario=usuario)

# Exercício 4
@app.route("/ex4")
def ex4():
    alunos = ["Ana", "Bruno", "Carlos", "Diana"]
    return render_template("ex4.html", alunos=alunos)

# Exercício 5
@app.route("/ex5")
def ex5():
    nota = 8
    return render_template("ex5.html", nota=nota)

if __name__ == "__main__":
    app.run(debug=True)
