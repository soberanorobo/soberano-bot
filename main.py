import os
from flask import Flask, request

app = Flask(__name__)

# Lê a variável VERIFY_TOKEN configurada no Render (padrão: "soberano 123")
VERIFY_TOKEN = os.environ.get("VERIFY_TOKEN", "soberano 123")


# Rota principal para verificar se o serviço está ativo no Render
@app.route("/", methods=["GET"])
def home():
    return "Bot Soberano Pet está ativo!", 200


# Rota do Webhook da Meta / WhatsApp
@app.route("/webhook", methods=["GET", "POST"])
def webhook():
    # 1. VERIFICAÇÃO DO WEBHOOK (Requisição GET enviada pela Meta)
    if request.method == "GET":
        mode = request.args.get("hub.mode")
        token = request.args.get("hub.verify_token")
        challenge = request.args.get("hub.challenge")

        # Compara o token enviado com a variável VERIFY_TOKEN
        if mode == "subscribe" and token == VERIFY_TOKEN:
            print("Webhook do Soberano verificado com sucesso!")
            # Retorna exatamente o valor do challenge com HTTP 200
            return challenge, 200
        else:
            print("Falha na verificação: token incorreto.")
            return "Token de verificação inválido", 403

    # 2. RECEBIMENTO DE MENSAGENS E EVENTOS (Requisição POST)
    elif request.method == "POST":
        data = request.json
        print("Mensagem recebida no Soberano Bot:", data)

        # A Meta exige resposta 200 OK imediata
        return "EVENT_RECEIVED", 200


if __name__ == "__main__":
    # O Render define a porta dinamicamente via variável de ambiente PORT
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
