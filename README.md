# Router Agent Framework

## Descrição
O Router Agent Framework é um sistema inteligente de processamento de mensagens que utiliza múltiplos agentes especializados para fornecer respostas adequadas a diferentes tipos de solicitações. O sistema emprega um roteador inteligente que direciona cada mensagem para o agente mais apropriado, mantendo um contexto personalizado para cada usuário através de um sistema de memória.

## Estrutura do Projeto
O projeto é composto pelos seguintes módulos:

- `main.py`: Módulo principal que gerencia a interface de usuário e o loop de interação
- `graph.py`: Implementa o grafo de fluxo de trabalho dos agentes e sua lógica de roteamento
- `models.py`: Configura os diferentes modelos de IA utilizados pelos agentes
- `prompts.py`: Define os prompts especializados para cada tipo de agente
- `state.py`: Define a estrutura de estado utilizada para gerenciar o contexto das interações

## Agentes Disponíveis

1. **Code Agent**: Especializado em gerar código com base nas instruções do usuário
2. **Thinking Agent**: Focado em resolver problemas complexos que requerem raciocínio elaborado
3. **Simple Agent**: Lida com interações conversacionais básicas

## Requisitos
- Python >=3.12
- Dependências listadas em `pyproject.toml`
- Chave de API para o Openrouter:


## Configuração

1. Clone o repositório
2. Instale as dependências:
```bash
uv sync
```
3. Configure as variáveis de ambiente em um arquivo `.env`:
```
BASE_URL=https://openrouter.ai/api/v1
OPENAI_API_KEY=sua chave de api OpenRouter
```

## Uso

Execute o programa principal:
```bash
uv run main.py
```

O sistema iniciará um prompt interativo onde você pode digitar suas mensagens. Para sair, digite 'sair'.

## Características

- **Roteamento Inteligente**: Seleciona automaticamente o melhor agente para cada tipo de solicitação
- **Memória Persistente**: Mantém contexto das interações anteriores para personalizar respostas
- **Múltiplos Modelos**: Utiliza diferentes modelos de IA otimizados para cada tipo de tarefa
- **Extensível**: Arquitetura modular permite adicionar novos agentes facilmente

## Contribuindo

1. Faça um fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request
