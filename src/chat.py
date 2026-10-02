from search import search_prompt

def main():
    chain = search_prompt()

    if not chain:
        print("Não foi possível iniciar o chat. Verifique os erros de inicialização.")
        return

    print("=" * 60)
    print("Chat iniciado! Digite sua pergunta ou 'sair' para encerrar.")
    print("=" * 60)

    while True:
        pergunta = input("\nPERGUNTA: ").strip()

        if not pergunta:
            continue

        if pergunta.lower() in ("sair", "exit", "quit"):
            print("Encerrando o chat. Até mais!")
            break

        resposta = chain(pergunta)
        print(f"\nRESPOSTA: {resposta}")


if __name__ == "__main__":
    main()