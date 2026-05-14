from flask import Flask

app = Flask(__name__)


@app.route("/")
def decorator():
    return """<!DOCTYPE html>
<html lang='pt-BR'>
<head>
  <meta charset='UTF-8'>
  <title>Currículo</title>
</head>
<body>

  <h1>Yago</h1>

  <p>Email: yago@email.com</p>
  <p>Telefone: (31) 99999-9999</p>
  <p>Cidade: Belo Horizonte - MG</p>

  <h2>Objetivo</h2>
  <p>Trabalhar na área de tecnologia.</p>

  <h2>Formação</h2>
  <p>Ensino Médio Completo</p>

  <h2>Habilidades</h2>
  <ul>
    <li>HTML</li>
    <li>CSS</li>
    <li>JavaScript</li>
  </ul>

</body>
</html>"
"""

if __name__ == "__main__":
    app.run(debug=True)




