"""
Router Agent Framework - Graph Module

Este módulo implementa um framework de agentes de IA com sistema de roteamento baseado em LangGraph.
O sistema utiliza diferentes modelos de linguagem para diferentes tipos de tarefas,
mantendo memória persistente para cada usuário.

O fluxo de trabalho é o seguinte:
1. Um roteador decide qual agente deve processar a mensagem do usuário
2. O agente selecionado processa a mensagem utilizando sua memória personalizada
3. A memória do usuário é atualizada com base na interação
"""

from langgraph.graph import StateGraph, END, START
from langgraph.checkpoint.memory import MemorySaver
from langgraph.store.memory import InMemoryStore
from langgraph.store.base import BaseStore

from langchain_core.messages import SystemMessage
from langchain_core.runnables import RunnableConfig

from prompts import (
    router_prompt,
    code_prompt,
    thinking_prompt,
    simple_prompt,
    memory_prompt,
)

from state import State
from models import llm_router, llm_code, llm_thinking, llm_basic

from dotenv import load_dotenv

load_dotenv()  # Carrega variáveis de ambiente do arquivo .env


def get_memory_content(config: RunnableConfig, store: BaseStore):
    """
    Recupera o conteúdo da memória armazenada para um usuário específico.

    Args:
        config: Configuração do Runnable contendo o ID do usuário
        store: Armazenamento onde a memória está guardada

    Returns:
        str: Conteúdo da memória do usuário ou mensagem padrão se não existir
    """
    user_id = config["configurable"]["user_id"]  # Obtém o ID do usuário da configuração
    namespace = ("memory", user_id)  # Define o namespace para armazenamento da memória
    key = "user_memory"  # Chave para acessar a memória do usuário
    existing_memory = store.get(namespace, key)  # Tenta recuperar a memória existente

    if existing_memory:
        return existing_memory.value.get(
            "memory"
        )  # Retorna o conteúdo da memória se existir
    else:
        return "No existing memory found."  # Retorna mensagem padrão se não existir memória


def router_node(state: State):
    """
    Nó de roteamento que decide qual agente específico deve processar a mensagem do usuário.

    Args:
        state: Estado atual contendo as mensagens do usuário

    Returns:
        dict: Contendo a decisão do agente a ser usado
    """
    agent = llm_router.invoke(
        [router_prompt] + state["messages"]
    )  # Invoca o modelo de roteamento
    return {"agent": agent.content}  # Retorna o nome do agente selecionado


def code_node(state: State, config: RunnableConfig, store: BaseStore):
    """
    Nó de agente especializado em gerar código com base nas instruções do usuário.

    Args:
        state: Estado atual contendo as mensagens do usuário
        config: Configuração do Runnable contendo o ID do usuário
        store: Armazenamento para acessar a memória do usuário

    Returns:
        dict: Contendo a resposta com o código gerado
    """
    memory_content = get_memory_content(config, store)  # Obtém a memória do usuário
    system_msg = code_prompt.format(
        memory=memory_content
    )  # Formata o prompt com a memória
    resp = llm_code.invoke(
        [system_msg] + state["messages"]
    )  # Invoca o modelo de geração de código
    return {"response": resp.content}  # Retorna a resposta contendo o código


def thinking_node(state: State, config: RunnableConfig, store: BaseStore):
    """
    Nó de agente que utiliza raciocínio detalhado para resolver problemas complexos.

    Args:
        state: Estado atual contendo as mensagens do usuário
        config: Configuração do Runnable contendo o ID do usuário
        store: Armazenamento para acessar a memória do usuário

    Returns:
        dict: Contendo a resposta após processo de raciocínio
    """
    memory_content = get_memory_content(config, store)  # Obtém a memória do usuário
    system_msg = thinking_prompt.format(
        memory=memory_content
    )  # Formata o prompt com a memória
    resp = llm_thinking.invoke(
        [system_msg] + state["messages"]
    )  # Invoca o modelo com capacidade de raciocínio
    return {
        "response": resp.content[1]["text"]
    }  # Retorna o texto de pensamento processado


def simple_node(state: State, config: RunnableConfig, store: BaseStore):
    """
    Nó de agente simplificado para respostas diretas e conversacionais.

    Args:
        state: Estado atual contendo as mensagens do usuário
        config: Configuração do Runnable contendo o ID do usuário
        store: Armazenamento para acessar a memória do usuário

    Returns:
        dict: Contendo a resposta direta ao usuário
    """
    memory_content = get_memory_content(config, store)  # Obtém a memória do usuário
    system_msg = simple_prompt.format(
        memory=memory_content
    )  # Formata o prompt com a memória
    resp = llm_basic.invoke([system_msg] + state["messages"])  # Invoca o modelo básico
    return {"response": resp.content}  # Retorna a resposta do modelo


def write_memory(state: State, config: RunnableConfig, store: BaseStore):
    """
    Reflete sobre o histórico de chat e salva uma memória personalizada no armazenamento.

    Args:
        state: Estado atual contendo as mensagens do usuário
        config: Configuração do Runnable contendo o ID do usuário
        store: Armazenamento para salvar a memória atualizada

    Returns:
        None: Esta função não retorna valores, apenas atualiza o armazenamento
    """

    # Obtém o ID do usuário da configuração
    user_id = config["configurable"]["user_id"]

    # Recupera a memória existente do armazenamento
    namespace = ("memory", user_id)
    existing_memory = store.get(namespace, "user_memory")

    # Extrai o conteúdo da memória
    if existing_memory:
        existing_memory_content = existing_memory.value.get("memory")
    else:
        existing_memory_content = "No existing memory found."

    # Formata a memória no prompt do sistema
    system_msg = memory_prompt.format(memory=existing_memory_content)
    new_memory = llm_basic.invoke(
        [SystemMessage(content=system_msg)] + state["messages"]
    )

    # Substitui a memória existente no armazenamento
    key = "user_memory"

    # Escreve o valor como um dicionário com uma chave de memória
    store.put(namespace, key, {"memory": new_memory.content})


def choose_agent(state: State):
    """
    Determina qual nó de agente será ativado com base na decisão do roteador.

    Args:
        state: Estado atual contendo a decisão do agente

    Returns:
        str: Nome do agente a ser utilizado
    """
    response = state["agent"]  # Obtém a decisão do roteador
    if response == "code_agent":
        return "code_agent"  # Retorna o agente de código
    elif response == "thinking_agent":
        return "thinking_agent"  # Retorna o agente de raciocínio
    elif response == "simple_agent":
        return "simple_agent"  # Retorna o agente simples
    else:
        return "simple_agent"  # Retorna o agente simples como fallback


def build_graph():
    """
    Constrói e compila o grafo de fluxo de trabalho dos agentes.

    Returns:
        Runnable: Grafo compilado pronto para execução
    """
    builder = StateGraph(State)  # Inicializa o construtor do grafo com o tipo State

    # Adiciona os nós ao grafo
    builder.add_node("router", router_node)  # Nó de roteamento
    builder.add_node("code_agent", code_node)  # Nó de agente de código
    builder.add_node("thinking_agent", thinking_node)  # Nó de agente de raciocínio
    builder.add_node("simple_agent", simple_node)  # Nó de agente simples
    builder.add_node("write_memory", write_memory)  # Nó para escrita de memória

    # Configura as arestas do grafo
    builder.add_edge(START, "router")  # Inicia com o roteador
    builder.add_conditional_edges(
        "router", choose_agent
    )  # Escolhe o agente baseado na decisão do roteador
    builder.add_edge(
        "router", "write_memory"
    )  # Conecta o roteador à escrita de memória

    builder.add_edge("write_memory", END)  # Finaliza o fluxo após escrita de memória

    # Compila e retorna o grafo
    return builder.compile(checkpointer=MemorySaver(), store=InMemoryStore())
