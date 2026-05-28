import math
from flask import render_template, request


def calcular():
    operacao = request.form.get("operacao", "+")
    num1_str = request.form.get("num1", "").strip()

    if not num1_str:
        return render_template("calculadora.html", etapas="Informe o primeiro número.", resultados="")

    num1 = float(num1_str)

    # --- Raiz quadrada (só num1) ---
    if operacao == "sqrt":
        if num1 < 0:
            return render_template("calculadora.html",
                                   etapas=f"Não existe raiz real de {num1}.",
                                   resultados="Erro: número negativo")
        resultado = math.sqrt(num1)
        return render_template("calculadora.html",
                               etapas=f"√{num1}",
                               resultados=resultado)

    # --- Logaritmo (só num1) ---
    if operacao == "log":
        if num1 <= 0:
            return render_template("calculadora.html",
                                   etapas=f"Logaritmo indefinido para {num1}.",
                                   resultados="Erro: número deve ser positivo")
        resultado = math.log(num1)
        return render_template("calculadora.html",
                               etapas=f"ln({num1})",
                               resultados=resultado)

    # --- Bhaskara (usa num1=a, num2=b, num3=c via form) ---
    if operacao == "bhaskara":
        b_str = request.form.get("num2", "").strip()
        c_str = request.form.get("num3", "").strip()
        if not b_str or not c_str:
            return render_template("calculadora.html",
                                   etapas="Informe a, b e c para Bhaskara.",
                                   resultados="")
        a, b, c = num1, float(b_str), float(c_str)
        delta = b**2 - 4 * a * c
        etapas = f"Δ = {b}² − 4×{a}×{c} = {delta}"
        if delta < 0:
            return render_template("calculadora.html",
                                   etapas=etapas,
                                   resultados="Sem raízes reais (Δ < 0)")
        x1 = (-b + math.sqrt(delta)) / (2 * a)
        x2 = (-b - math.sqrt(delta)) / (2 * a)
        resultados = f"x₁ = {x1}  |  x₂ = {x2}" if delta > 0 else f"x = {x1}"
        return render_template("calculadora.html", etapas=etapas, resultados=resultados)

    # --- Operações binárias (num1 op num2) ---
    num2_str = request.form.get("num2", "").strip()
    if not num2_str:
        return render_template("calculadora.html",
                               etapas="Informe o segundo número para esta operação.",
                               resultados="")
    num2 = float(num2_str)

    ops = {
        "+":  (lambda a, b: a + b,  f"{num1} + {num2}"),
        "-":  (lambda a, b: a - b,  f"{num1} − {num2}"),
        "*":  (lambda a, b: a * b,  f"{num1} × {num2}"),
        "/":  (lambda a, b: a / b,  f"{num1} ÷ {num2}"),
        "**": (lambda a, b: a ** b, f"{num1} ^ {num2}"),
    }

    if operacao not in ops:
        return render_template("calculadora.html", etapas="Operação inválida.", resultados="")

    fn, etapas = ops[operacao]

    if operacao == "/" and num2 == 0:
        return render_template("calculadora.html",
                               etapas=etapas,
                               resultados="Erro: divisão por zero")

    resultado = fn(num1, num2)
    return render_template("calculadora.html", etapas=etapas, resultados=resultado)
