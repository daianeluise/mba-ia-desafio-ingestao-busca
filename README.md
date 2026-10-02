# Desafio: Ingestão e Busca Semântica com LangChain e PostgreSQL

## Objetivo

Implementar uma aplicação em Python para:

- ler um arquivo PDF,
- dividir o conteúdo em chunks,
- gerar embeddings,
- armazenar os vetores em um banco PostgreSQL com extensão pgVector,
- permitir consultas em linguagem natural via CLI,
- responder apenas com base no contexto recuperado do banco.

## Funcionalidade esperada

A aplicação deve simular um chat no terminal, em que o usuário digita uma pergunta e o sistema:

1. gera o embedding da pergunta;
2. busca os 10 documentos mais relevantes no banco vetorial;
3. monta o prompt com o contexto recuperado;
4. chama a LLM;
5. retorna a resposta ao usuário.

Exemplo de interação:

```text
PERGUNTA: Qual o faturamento da Empresa SuperTechIABrazil?
RESPOSTA: O faturamento foi de 10 milhões de reais.

PERGUNTA: Quantos clientes temos em 2024?
RESPOSTA: Não tenho informações necessárias para responder sua pergunta.
```

## Tecnologias utilizadas

- Python
- LangChain
- PostgreSQL + pgVector
- Docker e Docker Compose
- OpenAI (embeddings e modelo de resposta)

## Estrutura do projeto

```text
.
├── .env.example
├── .env
├── docker-compose.yml
├── requirements.txt
├── README.md
├── document.pdf
└── src/
    ├── chat.py
    ├── ingest.py
    └── search.py
```

## Pré-requisitos

- Python 3.10+
- Docker e Docker Compose instalados
- Conta e chave da API da OpenAI

## Configuração do ambiente

Crie um ambiente virtual e instale as dependências:

```bash
python -m venv .venv
. .venv/bin/activate
# no Windows PowerShell:
# .\.venv\Scripts\Activate.ps1

pip install -r requirements.txt
```

Configure as variáveis de ambiente em um arquivo `.env` na raiz do projeto. Use o arquivo [.env.example](.env.example) como modelo.

Conteúdo esperado:

```env
OPENAI_API_KEY=sua_chave_aqui
OPENAI_EMBEDDING_MODEL=text-embedding-3-small
OPENAI_CHAT_MODEL=gpt-4o-mini
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/rag
PG_VECTOR_COLLECTION_NAME=desafioingest_collection
PDF_PATH=document.pdf
```

Observações:

- O modelo de embedding e o modelo de resposta podem variar conforme a documentação oficial do provedor escolhido.
- Se você trocar o modelo de embeddings após uma ingestão anterior, a coleção vetorial pode ficar incompatível e será necessário recriar a tabela/coleção.

## Ordem de execução

1. Subir o banco de dados:

```bash
docker compose up -d
```

2. Executar a ingestão do PDF:

```bash
python src/ingest.py
```

3. Iniciar o chat:

```bash
python src/chat.py
```

## Prompt usado para a resposta

O sistema usa o seguinte formato para enviar o contexto e a pergunta para a LLM:

```text
CONTEXTO:
{contexto}

REGRAS:
- Responda somente com base no CONTEXTO.
- Se a informação não estiver explicitamente no CONTEXTO, responda:
  "Não tenho informações necessárias para responder sua pergunta."
- Nunca invente ou use conhecimento externo.
- Nunca produza opiniões ou interpretações além do que está escrito.

EXEMPLOS DE PERGUNTAS FORA DO CONTEXTO:
Pergunta: "Qual é a capital da França?"
Resposta: "Não tenho informações necessárias para responder sua pergunta."

Pergunta: "Quantos clientes temos em 2024?"
Resposta: "Não tenho informações necessárias para responder sua pergunta."

Pergunta: "Você acha isso bom ou ruim?"
Resposta: "Não tenho informações necessárias para responder sua pergunta."

PERGUNTA DO USUÁRIO:
{pergunta}

RESPONDA A "PERGUNTA DO USUÁRIO"
```

## Requisitos de entrega

O projeto deve conter:

- código-fonte completo,
- instruções claras de execução,
- arquivo de variáveis de ambiente,
- banco PostgreSQL em Docker,
- ingestão do PDF,
- busca semântica com relevância,
- CLI interativo para perguntas ao usuário.

## Observação final

Este desafio exige que a resposta da IA seja estritamente baseada no conteúdo do PDF carregado no banco vetorial. Caso a informação não esteja presente no contexto, a aplicação deve responder com a mensagem padronizada:

```text
Não tenho informações necessárias para responder sua pergunta.
```
