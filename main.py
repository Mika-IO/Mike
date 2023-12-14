import os
import openai
import speech_recognition as sr
import pyttsx3
from dotenv import load_dotenv

load_dotenv()

# Configurar a chave da API da OpenAI
openai.api_key = os.getenv("OPEN_API_KEY")


def ouvir_usuario():
    # Inicializar o reconhecedor de voz
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Fale algo...")
        audio = r.listen(source)

    try:
        text = r.recognize_google(audio)
        return text
    except sr.UnknownValueError:
        return "Não entendi"
    except sr.RequestError:
        return "Erro no serviço de reconhecimento de voz"


def responder(texto):
    # Enviar a pergunta para a API da OpenAI
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "user", "content": "Seu nome é mike, tu é um assistente virtual"},
            {"role": "user", "content": texto},
        ],
    )

    return response.choices[0].message["content"]


def falar(texto):
    # Inicializar o sintetizador de voz
    engine = pyttsx3.init()
    voices = engine.getProperty("voices")
    for voice in voices:
        print("Voice:", voice.id)
    engine.setProperty("voice", voices[0].id)  # for example, select the first voice
    engine.say(texto)
    engine.runAndWait()


def main():
    while True:
        texto_usuario = ouvir_usuario()
        if texto_usuario.lower() == "pare":
            break

        resposta = responder(texto_usuario)
        print("Mike:", resposta)
        falar(resposta)


if __name__ == "__main__":
    main()
