"""
Módulo Principal - Router Agent Framework

Este é o módulo principal que inicializa e executa o framework de agentes.
Ele configura o ambiente de execução e gerencia o loop principal de interação com o usuário.
"""

from langchain_core.messages import HumanMessage
from uuid import uuid4

from graph import build_graph

# Inicializa o grafo de agentes
graph = build_graph()

# Configuração única para identificação da sessão e usuário
id = str(uuid4())
config = {"configurable": {"thread_id": id, "user_id": id}}


def main():
    """
    Função principal que executa o loop de interação com o usuário.

    O loop continua até que o usuário digite 'sair'.
    Cada mensagem do usuário é processada pelo grafo de agentes,
    que seleciona o agente apropriado e gera uma resposta.
    """
    print("Digite 'sair' ou pressione CTRL+C para encerrar.")
    try:
        while True:
            messages = HumanMessage(content=input("Usuário: "))
            if messages.content == "sair":
                break
            resp = graph.invoke({"messages": [messages]}, config, debug=True)

            print("Assistente: ", resp["response"])
    except KeyboardInterrupt:
        print("\nPrograma encerrado pelo usuário.")


if __name__ == "__main__":
    main()
