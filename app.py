# GET  /              → abre o dashboard visual
# POST /adicionar     → adiciona uma tarefa na fila
# GET  /status        → retorna o estado atual da fila
# GET  /resetar       → reseta tudo para testar de novo

from flask import Flask, render_template, request, jsonify
from queue_manager import QueueManager

app = Flask(__name__)

# Fila com máximo de 10 tarefas e 2 segundos de processamento cada
fila = QueueManager(max_size=10, process_time=2.0)

# ─── DASHBOARD ───────────────────────────────────────────
@app.route("/")
def index():
    return render_template("index.html")

# ─── ADICIONAR TAREFA NA FILA ────────────────────────────
@app.route("/adicionar", methods=["POST"])
def adicionar():
    """
    Recebe a requisição e tenta adicionar na fila.
    Retorna 200 se aceito, 503 se fila cheia.
    """
    data    = request.get_json()
    user_id = data.get("user_id", "usuario_1")
    result  = fila.adicionar(user_id)

    # 200 = aceito, 503 = serviço indisponível (fila cheia)
    status_code = 200 if result["allowed"] else 503
    return jsonify(result), status_code

# ─── STATUS DA FILA ──────────────────────────────────────
@app.route("/status")
def status():
    """Retorna o estado atual de toda a fila em JSON."""
    return jsonify(fila.status())

# ─── RESETAR ─────────────────────────────────────────────
@app.route("/resetar")
def resetar():
    """Reseta toda a fila para testar novamente."""
    fila.resetar()
    return jsonify({"message": "✅ Fila resetada!"})

if __name__ == "__main__":
    app.run(debug=True)