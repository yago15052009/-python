from flask import Flask, request, render_template

app = Flask(__name__)

usuarios = {
    'yago': '22400508',
    'dolga': 'cotemig2026',
    'janaina': 'cotemig2026',
    'antonio': 'cotemig2026',
}

def show_the_login_form():
    return render_template('login.html')

def do_the_login():
    usuario = request.form.get('usuario')
    senha = request.form.get('senha')

    for user, pwd in usuarios.items():
        if usuario == user and senha == pwd:
            return f"<h1>Bem-vindo, {usuario}!</h1>"

    return "<h1>Login inválido</h1>"

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        return do_the_login()
    else:
        return show_the_login_form()

if __name__ == "__main__":
    app.run(debug=True)


