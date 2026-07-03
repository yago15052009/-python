from flask import Flask, render_template, request

app = Flask(__name__)

dados_especialidades = {
    "Cardiologia": [
        {"nome": "Dr. André Souza",    "crm": "CRM/MG 18432", "planos": ["Unimed", "Amil", "SulAmérica"]},
        {"nome": "Dra. Fernanda Melo", "crm": "CRM/MG 22105", "planos": ["Bradesco Saúde", "Unimed"]},
    ],
    "Pediatria": [
        {"nome": "Dra. Carla Nunes",   "crm": "CRM/MG 15780", "planos": ["Unimed", "Hapvida", "Amil"]},
        {"nome": "Dr. Lucas Ribeiro",  "crm": "CRM/MG 31209", "planos": ["SulAmérica", "NotreDame"]},
    ],
    "Dermatologia": [
        {"nome": "Dra. Juliana Costa", "crm": "CRM/MG 29801", "planos": ["Amil", "Bradesco Saúde"]},
    ],
}

@app.route("/", methods=["GET", "POST"])
def index():
    medicos = None
    especialidade = None
    input_valor = ""
    erro = None

    if request.method == "POST":
        input_valor = request.form.get("especialidade", "").strip()
        especialidade = input_valor.title()

        if not especialidade:
            erro = "Por favor, digite uma especialidade."
        else:
            medicos = dados_especialidades.get(especialidade)
            if medicos is None:
                erro = f'Nenhum médico encontrado para "{especialidade}".'
                especialidade = None

    return render_template("index.html",
                           medicos=medicos,
                           especialidade=especialidade,
                           input_valor=input_valor,
                           erro=erro)

if __name__ == "__main__":
    app.run(debug=True)
