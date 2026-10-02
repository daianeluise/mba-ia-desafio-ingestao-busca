# Desafio: Ingestão e Busca Semântica com LangChain e PostgreSQL

## Objetivo

Implementar uma aplicação em Python capaz de:

- ler um arquivo PDF;
- dividir o conteúdo em chunks;
- gerar embeddings;
- armazenar os vetores em um banco PostgreSQL com a extensão pgVector;
- permitir consultas em linguagem natural via CLI;
- responder apenas com base no contexto recuperado do banco.

## Funcionalidade esperada

A aplicação simula um chat no terminal. Ao receber uma pergunta, o sistema:

1. gera o embedding da pergunta;
2. busca os 10 documentos mais relevantes no banco vetorial (k=10);
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

- Python 3.10+
- LangChain
- PostgreSQL + pgVector
- Docker e Docker Compose
- OpenAI (embeddings e modelo de resposta)

## Estrutura do projeto

```text
.
├── .env.example
├── .env
├── .gitignore
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

- Python 3.10+ instalado
- Docker e Docker Compose instalados
- Conta e chave da API da OpenAI

## Configuração do ambiente

Crie e ative um ambiente virtual e instale as dependências:

```bash
python -m venv .venv
# Linux/macOS:
source .venv/bin/activate
# Windows PowerShell:
.\.venv\Scripts\Activate.ps1

pip install -r requirements.txt
```

Configure as variáveis de ambiente em um arquivo `.env` na raiz do projeto, usando o `.env.example` como modelo:

```env
OPENAI_API_KEY=sua_chave_aqui
OPENAI_EMBEDDING_MODEL=text-embedding-3-small
OPENAI_CHAT_MODEL=gpt-4o-mini
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/rag
PG_VECTOR_COLLECTION_NAME=desafioingest_collection
PDF_PATH=document.pdf
```

> ⚠️ O `.env` contém sua chave da API e **não deve ser versionado**. O `.gitignore` já exclui `.env`, `venv/` e `__pycache__/`.

## Banco de dados com Docker

O `docker-compose.yml` sobe um PostgreSQL com a extensão pgVector:

```yaml
services:
  postgres:
    image: pgvector/pgvector:pg17
    container_name: postgres_rag
    environment:
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: postgres
      POSTGRES_DB: rag
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U postgres -d rag"]
      interval: 10s
      timeout: 5s
      retries: 5
    restart: unless-stopped

  bootstrap_vector_ext:
    image: pgvector/pgvector:pg17
    depends_on:
      postgres:
        condition: service_healthy
    entrypoint: ["/bin/sh", "-c"]
    command: >
      PGPASSWORD=postgres
      psql "postgresql://postgres@postgres:5432/rag" -v ON_ERROR_STOP=1
      -c "CREATE EXTENSION IF NOT EXISTS vector;"
    restart: "no"

volumes:
  postgres_data:
```

> ⚠️ Se você tiver um PostgreSQL instalado localmente, pare o serviço antes de subir o container, pois ambos usam a porta 5432. No Windows (PowerShell como administrador):
> ```powershell
> Stop-Service postgresql-x64-15
> ```

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

## Verificando a ingestão

Para conferir se os dados foram gravados no banco:

```bash
docker exec -it postgres_rag psql -U postgres -d rag -c "SELECT count(*) FROM langchain_pg_embedding;"
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

## Observações

- Se você trocar o modelo de embeddings após uma ingestão anterior, a collection pode ficar incompatível (dimensões diferentes) e será necessário recriar a tabela/coleção e refazer a ingestão do zero.
- Os modelos de embedding e de resposta podem variar conforme a documentação oficial do provedor escolhido.

## Requisitos de entrega

O projeto deve conter:

- código-fonte completo;
- instruções claras de execução;
- arquivo de variáveis de ambiente (`.env.example`);
- banco PostgreSQL em Docker;
- ingestão do PDF;
- busca semântica com relevância;
- CLI interativo para perguntas ao usuário.

## Entregável

Repositório público no GitHub contendo todo o código-fonte e este README com instruções claras de execução do projeto.
