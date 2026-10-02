import os
from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_postgres import PGVector

PROMPT_TEMPLATE = """
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
"""


def search_prompt(question=None):
   
    load_dotenv()

    for key in ("DATABASE_URL", "PG_VECTOR_COLLECTION_NAME", "OPENAI_API_KEY", "OPENAI_EMBEDDING_MODEL"):
      if not os.getenv(key):
        raise RuntimeError(f"{key} variavel de ambiente não definida.")

    embeddings = OpenAIEmbeddings(
          model=os.getenv("OPENAI_EMBEDDING_MODEL","text-embedding-3-small")
      )

    store = PGVector(
          connection=os.getenv("DATABASE_URL"),
          collection_name=os.getenv("PG_VECTOR_COLLECTION_NAME"),
          embeddings=embeddings,
          use_jsonb=True,
      ) 
  
    llm = ChatOpenAI(model=os.getenv("OPENAI_CHAT_MODEL", "gpt-4o-mini"))

    if question is not None:
        if not str(question).strip():
            raise ValueError("A pergunta não pode ser vazia.")

        docs = store.similarity_search(question, k=10)
        contexto = "\n\n".join(doc.page_content for doc in docs)
        return PROMPT_TEMPLATE.format(contexto=contexto, pergunta=question)

    def chain(pergunta):
        if not pergunta or not str(pergunta).strip():
            raise ValueError("A pergunta não pode ser vazia.")

        docs = store.similarity_search(pergunta, k=10)
        contexto = "\n\n".join(doc.page_content for doc in docs)
        prompt = PROMPT_TEMPLATE.format(contexto=contexto, pergunta=pergunta)

        resposta = llm.invoke(prompt)
        return resposta.content

    return chain
