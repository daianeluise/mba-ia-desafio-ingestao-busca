import os
from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_postgres import PGVector
from pathlib import Path
from langchain_openai import OpenAIEmbeddings
from langchain_core.documents import Document


load_dotenv()

for key in ("DATABASE_URL", "PG_VECTOR_COLLECTION_NAME", "OPENAI_API_KEY", "OPENAI_EMBEDDING_MODEL", "PDF_PATH"):
   if not os.getenv(key):
        raise RuntimeError(f"{key} variavel de ambiente não definida.")

PDF_PATH = os.getenv("PDF_PATH")

def ingest_pdf():
    loader = PyPDFLoader(PDF_PATH)
    pages = loader.load()

    docs = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=150).split_documents(pages)
    print(f"Chunks gerados: {len(docs)}")

    if not docs:
         raise RuntimeError(
            "Nenhum chunk gerado."
        )

    docEnriquecido = [
        Document(
            page_content=doc.page_content,
            metadata={chave: valor for chave, valor in doc.metadata.items() if chave not in ("", None)}    ,
        )
        for doc in docs  
    ]    

    embeddings = OpenAIEmbeddings(
        model=os.getenv("OPENAI_EMBEDDING_MODEL","text-embedding-3-small")
    )

    store = PGVector(
        connection=os.getenv("DATABASE_URL"),
        collection_name=os.getenv("PG_VECTOR_COLLECTION_NAME"),
        embeddings=embeddings,
        use_jsonb=True,
    )

    ids = [f"doc-{i}" for i in range(len(docEnriquecido))]
    store.add_documents(documents=docEnriquecido, ids=ids)

    print(f"✅ Ingestão concluída: {len(docEnriquecido)} documentos gravados no banco.")


if __name__ == "__main__":
    ingest_pdf()