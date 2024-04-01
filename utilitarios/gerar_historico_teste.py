import os
import json
import datetime
import random

def gerar_historico(qtd=10):
    if not os.path.exists("history"):
        os.makedirs("history")

    for i in range(qtd):
        timestamp = datetime.datetime.now() - datetime.timedelta(days=i)
        ts_str = timestamp.strftime("%Y%m%d_%H%M%S")

        dados = {
            "id": f"session_{ts_str}",
            "timestamp": str(timestamp),
            "messages": [
                {"role": "user", "content": f"Teste de mensagem {i}"},
                {"role": "assistant", "content": f"Resposta teste {i}"}
            ]
        }

        with open(f"history/session_{ts_str}.json", 'w') as f:
            json.dump(dados, f)

    print(f"Gerados {qtd} arquivos de histórico em 'history/'.")

if __name__ == "__main__":
    gerar_historico(12)
