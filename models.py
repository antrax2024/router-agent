"""
Módulo Models - Router Agent Framework

Este módulo configura os diferentes modelos de linguagem utilizados pelos agentes.
Cada modelo é especializado em um tipo específico de tarefa:
- llm_router: Modelo para decisão de roteamento (Gemini Flash 2.0)
- llm_code: Modelo especializado em geração de código (Claude 3.7 Sonnet)
- llm_thinking: Modelo para raciocínio complexo (Claude 3.7 Sonnet com tokens estendidos)
- llm_basic: Modelo para respostas simples (DeepSeek V3)
"""

from langchain_openai import ChatOpenAI
import os
from dotenv import load_dotenv

load_dotenv()
BASE_URL: str | None = os.getenv(key="BASE_URL")
OPENAI_API_KEY: str | None = os.getenv(key="OPENAI_API_KEY")

# Definição do modelo base Claude para tarefas complexas
model = "anthropic/claude-3.7-sonnet"

# Modelo Gemini otimizado para decisões rápidas de roteamento
llm_router = ChatOpenAI(
    base_url=BASE_URL,
    openai_api_key=OPENAI_API_KEY,
    model="google/gemini-2.0-flash-001",
    temperature=0,
)

# Modelo Claude especializado em geração de código
llm_code = ChatOpenAI(
    base_url=BASE_URL,
    openai_api_key=OPENAI_API_KEY,
    model=model,
    temperature=0.7,
)

# Modelo Claude configurado para raciocínio profundo com tokens estendidos
llm_thinking = ChatOpenAI(
    base_url=BASE_URL,
    openai_api_key=OPENAI_API_KEY,
    model=model,
    max_tokens=20000,
    thinking={"type": "enabled", "budget_tokens": 16000},
)

# Modelo DeepSeek para respostas conversacionais simples
llm_basic = ChatOpenAI(
    model="deepseek/deepseek-chat",
    base_url=BASE_URL,
    openai_api_key=OPENAI_API_KEY,
    temperature=0.9,
)
