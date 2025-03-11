"""
Módulo State - Router Agent Framework

Este módulo define o tipo State utilizado em todo o Framework Router Agent.
A classe State representa o estado atual de uma conversa e interação do agente.
"""

from typing import TypedDict, List
from langchain_core.messages import BaseMessage

class State(TypedDict):
    """
    Representa o estado de uma interação do agente.
    
    Atributos:
        messages (List[BaseMessage]): Lista de mensagens na conversa atual
        agent (str): O tipo de agente selecionado para processar a mensagem atual
        response (str): A resposta gerada pelo agente selecionado
    """
    messages: List[BaseMessage]
    agent : str
    response: str

    