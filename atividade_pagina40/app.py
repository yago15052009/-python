from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from database import get_db, init_db
from functools import wraps
import requests

app = Flask(__name__)
app.secret_key = "chave-secreta-troque-em-producao"

# ── helpers ──────────────────────────────────────────────────────────────────

def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if "usuario_id" not in session:
            return redirect(url_for("login"))
        return f(*args, **kwargs)
    return decorated

def frase_motivacional():
    try:
        r = requests.get("https://api.adviceslip.com/advice", timeout=3)
        return r.json()["slip"]["advice"]
    except Exception:
        return "Foque no que você pode controlar."

# ── auth ─────────────────────────────────────────────────────────────────────

@app.route("/")
def index():
    return redirect(url_for("dashboard") if "usuario_id" in session else url_for("login"))

@app.route("/login", methods=["GET", "POST"])
def login():
    erro = None
    if request.method == "POST":
        email = request.form["email"].strip()
        senha = request.form["senha"]
        with get_db() as con:
            user = con.execute("SELECT * FROM usuarios WHERE email=?", (email,)).fetchone()
        if user and check_password_hash(user["senha"], senha):
            session["usuario_id"] = user["id"]
            session["usuario_nome"] = user["nome"]
            return redirect(url_for("dashboard"))
        erro = "E-mail ou senha inválidos."
    return render_template("login.html", erro=erro)

@app.route("/registro", methods=["GET", "POST"])
def registro():
    erro = None
    if request.method == "POST":
        nome  = request.form["nome"].strip()
        email = request.form["email"].strip()
        senha = request.form["senha"]
        if not nome or not email or not senha:
            erro = "Preencha todos os campos."
        else:
            try:
                with get_db() as con:
                    con.execute(
                        "INSERT INTO usuarios (nome, email, senha) VALUES (?,?,?)",
                        (nome, email, generate_password_hash(senha))
                    )
                return redirect(url_for("login"))
            except Exception:
                erro = "E-mail já cadastrado."
    return render_template("registro.html", erro=erro)

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))

# ── dashboard ─────────────────────────────────────────────────────────────────

@app.route("/dashboard")
@login_required
def dashboard():
    status_filtro = request.args.get("status", "todos")
    uid = session["usuario_id"]
    with get_db() as con:
        if status_filtro == "todos":
            tarefas = con.execute(
                "SELECT * FROM tarefas WHERE usuario_id=? ORDER BY id DESC", (uid,)
            ).fetchall()
        else:
            tarefas = con.execute(
                "SELECT * FROM tarefas WHERE usuario_id=? AND status=? ORDER BY id DESC",
                (uid, status_filtro)
            ).fetchall()
        totais = {
            row["status"]: row["total"]
            for row in con.execute(
                "SELECT status, COUNT(*) total FROM tarefas WHERE usuario_id=? GROUP BY status", (uid,)
            ).fetchall()
        }
    frase = frase_motivacional()
    return render_template("dashboard.html",
                           tarefas=tarefas,
                           frase=frase,
                           status_filtro=status_filtro,
                           totais=totais)

# ── API JSON ──────────────────────────────────────────────────────────────────

@app.route("/api/tarefas")
@login_required
def api_tarefas():
    status = request.args.get("status", "todos")
    uid = session["usuario_id"]
    with get_db() as con:
        if status == "todos":
            rows = con.execute(
                "SELECT * FROM tarefas WHERE usuario_id=? ORDER BY id DESC", (uid,)
            ).fetchall()
        else:
            rows = con.execute(
                "SELECT * FROM tarefas WHERE usuario_id=? AND status=? ORDER BY id DESC",
                (uid, status)
            ).fetchall()
    return jsonify([dict(r) for r in rows])

@app.route("/api/progresso")
@login_required
def api_progresso():
    uid = session["usuario_id"]
    with get_db() as con:
        rows = con.execute(
            "SELECT status, COUNT(*) total FROM tarefas WHERE usuario_id=? GROUP BY status", (uid,)
        ).fetchall()
    return jsonify({r["status"]: r["total"] for r in rows})

# ── CRUD tarefas ──────────────────────────────────────────────────────────────

@app.route("/nova_tarefa", methods=["GET", "POST"])
@login_required
def nova_tarefa():
    erro = None
    if request.method == "POST":
        titulo    = request.form["titulo"].strip()
        descricao = request.form.get("descricao", "").strip()
        status    = request.form.get("status", "pendente")
        if not titulo:
            erro = "O título é obrigatório."
        else:
            with get_db() as con:
                con.execute(
                    "INSERT INTO tarefas (titulo, descricao, status, usuario_id) VALUES (?,?,?,?)",
                    (titulo, descricao, status, session["usuario_id"])
                )
            return redirect(url_for("dashboard"))
    return render_template("nova_tarefa.html", erro=erro)

@app.route("/editar/<int:id>", methods=["GET", "POST"])
@login_required
def editar(id):
    uid = session["usuario_id"]
    with get_db() as con:
        tarefa = con.execute(
            "SELECT * FROM tarefas WHERE id=? AND usuario_id=?", (id, uid)
        ).fetchone()
    if not tarefa:
        return redirect(url_for("dashboard"))
    erro = None
    if request.method == "POST":
        titulo    = request.form["titulo"].strip()
        descricao = request.form.get("descricao", "").strip()
        status    = request.form.get("status", tarefa["status"])
        if not titulo:
            erro = "O título é obrigatório."
        else:
            with get_db() as con:
                con.execute(
                    "UPDATE tarefas SET titulo=?, descricao=?, status=? WHERE id=? AND usuario_id=?",
                    (titulo, descricao, status, id, uid)
                )
            return redirect(url_for("dashboard"))
    return render_template("editar.html", tarefa=tarefa, erro=erro)

@app.route("/excluir/<int:id>", methods=["POST"])
@login_required
def excluir(id):
    with get_db() as con:
        con.execute(
            "DELETE FROM tarefas WHERE id=? AND usuario_id=?", (id, session["usuario_id"])
        )
    return redirect(url_for("dashboard"))

# ── progresso ─────────────────────────────────────────────────────────────────

@app.route("/progresso")
@login_required
def progresso():
    return render_template("progresso.html")

# ── main ──────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    init_db()
    app.run(debug=True)
