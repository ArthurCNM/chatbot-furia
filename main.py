import requests
import ollama

# API_KEY da PandaScore
API_KEY = ""
furia_id = 129853  # ID da FURIA no PandaScore

headers = {
    "Authorization": f"Bearer {API_KEY}"
}

# Prompt do sistema para o chatbot
system_prompt = (
    "Você deve responder sempre em *português brasileiro*. "
    "Você é um especialista em CS2 da FURIA eSports. "
    "Responda perguntas com entusiasmo e conhecimento sobre os times, jogadores, história e conquistas da FURIA. "
    "Atual lineup de CS da furia: A lineup atual da FURIA de CS é formada por Fallen, Kscerato, Yuurih, Molodoy e Yekindar. "
    "Fallen cujo nome real é Gabriel Toledo, ele é o capitão da FURIA. "
    "Molodoy é o AWPER da FURIA. "
    "Próximo jogo da FURIA CS: A FURIA enfrenta a The Mongolz no dia 10 de maio, às 5h pela PGL Astana. "
    "A FURIA tem sede em São Paulo, mas também possui operações nos EUA. "
    "A FURIA foi fundada em 2017. "
    "Os maiores títulos de CS2 da FURIA são: ESL Pro League Season 12 NA, DreamHack Masters Spring 2020 NA, IEM New York 2020 NA e Elisa Masters Espoo 2023."
)

PRESETS = {
    "1": {
        "pergunta": "Qual a atual lineup de CS da FURIA?",
        "resposta": "A lineup atual da FURIA de CS é formada por Fallen, Kscerato, Yuurih, Molodoy e Yekindar."
    },
    "2": {
        "pergunta": "Quando a FURIA foi fundada?",
        "resposta": "A FURIA foi fundada em 2017, com o objetivo de transformar o cenário competitivo brasileiro."
    },
    "3": {
        "pergunta": "Onde a FURIA está sediada?",
        "resposta": "A FURIA tem sede em São Paulo, mas também possui operações nos EUA."
    },
    "4": {
        "pergunta": "Quais os maiores títulos da FURIA?",
        "resposta": "ESL Pro League Season 12 NA, DreamHack Masters Spring 2020 NA, IEM New York 2020 NA e Elisa Masters Espoo 2023"
    },
    "5": {
        "pergunta": "Qual o próximo jogo da FURIA?",
        "resposta": None  
    },
    "6": {
        "pergunta": "Qual a primeira line da FURIA?",
        "resposta": "caike, VINI, spacca, prd e guerri"
    },
    "7": {
        "pergunta": "Quero fazer uma pergunta personalizada.",
        "resposta": None
    }
}

# Função para obter o próximo jogo da FURIA
def obter_partidas_furia():
    url = f"https://api.pandascore.co/csgo/matches/upcoming?filter[opponent_id]={furia_id}"

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        jogos = response.json()
        if not jogos:
            print("📭 A FURIA não tem partidas marcadas no momento.")
        else:
            jogo = jogos[0]
            nome_jogo = jogo.get("name", "Nome não disponível")
            torneio = jogo.get("tournament", {}).get("name", "Torneio não disponível")
            data_inicio = jogo.get("begin_at", "Data não disponível")

            print(f"🆚 {nome_jogo}")
            print(f"🏆 Torneio: {torneio}")
            print(f"🕒 Início: {data_inicio}")
            print("-" * 40)
    else:
        print(f"❌ Erro ao buscar partidas da FURIA: {response.status_code} - {response.text}")

# Função para interagir com o usuário
def chat_furia():
    print("🤖 Chatbot FURIOSO ativado!\n")
    messages = [{"role": "system", "content": system_prompt}]

    while True:
        exibir_menu()
        escolha = input("Sua escolha: ").strip().lower()

        if escolha in ["sair", "exit", "quit"]:
            print("🤖 Até mais! GO FURIA!")
            break

        if escolha in PRESETS:
            pergunta = PRESETS[escolha]["pergunta"]
            resposta_fixa = PRESETS[escolha]["resposta"]

            if resposta_fixa:
                print(f"FURIAbot: {resposta_fixa}\n")
            else:

                if escolha == "5":  # Próximo jogo da FURIA
                    print("FURIAbot: A FURIA tem o seguinte jogo marcado:\n")
                    obter_partidas_furia()
                else:
                    user_input = input("Digite sua pergunta: ").strip()
                    messages.append({"role": "user", "content": user_input})
                    reply = ""
                    for chunk in ollama.chat(model="llama3:8b", messages=messages, stream=True):
                        content = chunk.get("message", {}).get("content", "")
                        print(content, end="", flush=True)
                        reply += content
                    print("\n")
                    messages.append({"role": "assistant", "content": reply})

        else:
            print("❌ Opção inválida. Tente novamente.\n")

# Função para exibir o menu
def exibir_menu():
    print("\n📋 Menu - Escolha uma pergunta:")
    for key, item in PRESETS.items():
        print(f"{key}. {item['pergunta']}")
    print("Digite 'sair' para encerrar.\n")

if __name__ == "__main__":
    chat_furia()
