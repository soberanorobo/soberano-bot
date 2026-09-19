import os
import time
from flask import Flask, request, jsonify

app = Flask(__name__)

# Configurações do Soberano Pets
ADMIN_1 = "5585991634564"  # Principal
ADMIN_2 = "5585991999241"  # Segunda aprovadora
PIX_KEY = "eae2396a-6954-4fbf-a6b6-d328455e4df8"

# Dicionário em memória para armazenar os pedidos ativos e a trava de prioridade
pedidos = {}

@app.route("/", methods=["GET"])
def home():
    return "Soberano Pets Bot rodando com sucesso!", 200

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json()
    
    if data and "message" in data:
        msg = data["message"].get("text", "").strip()
        sender = data["message"].get("from", "")
        
        # Lógica de aprovação "primeiro a clicar/responder"
        if msg.startswith("OK_PEDIDO_"):
            pedido_id = msg.replace("OK_PEDIDO_", "")
            
            if pedido_id in pedidos:
                if pedidos[pedido_id]["status"] == "PENDENTE":
                    pedidos[pedido_id]["status"] = "APROVADO"
                    pedidos[pedido_id]["aprovado_por"] = sender
                    
                    return jsonify({
                        "status": "success",
                        "message": f"Pedido {pedido_id} aprovado por {sender}! Chave Pix enviada ao cliente."
                    })
                else:
                    aprovador = pedidos[pedido_id].get("aprovado_por", "outro administrador")
                    return jsonify({
                        "status": "already_approved",
                        "message": f"Pedido {pedido_id} já foi aprovado anteriormente por {aprovador}!"
                    })
            else:
                return jsonify({"status": "not_found", "message": "Pedido não encontrado."})

    return jsonify({"status": "ignored"}), 200

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
