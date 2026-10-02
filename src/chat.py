import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from search import search_prompt

load_dotenv()


def main():
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY não definida. Verifique o arquivo .env na raiz do projeto.")

    llm = ChatOpenAI(
        model=os.getenv("OPENAI_CHAT_MODEL", "gpt-4o-mini"),
        api_key=api_key,
    )

    print("=" * 60)
    print("Chat iniciado! Digite sua pergunta ou 'sair' para encerrar.")
    print("=" * 60)

    while True:
        pergunta = input("\nPERGUNTA: ").strip()

        if not pergunta:
            continue

        if pergunta.lower() in ("sair", "exit", "quit"):
            print("Encerrando o chat. Até mais! 👋")
            break

        prompt = search_prompt(pergunta)
        resposta = llm.invoke(prompt)
        print(f"\nRESPOSTA: {resposta.content}")

if __name__ == "__main__":
    main()