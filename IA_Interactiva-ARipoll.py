
import requests
import base64
import speech_recognition as sr
from pydub import AudioSegment
from PIL import Image
from io import BytesIO

URL_CHAT = "http://192.168.0.12:1234/v1/chat/completions"
HEADERS = {"Content-Type": "application/json"}

def consultarModelo(prompt,imagen_b64=None, audio_b64=None):

    data = {
        "model": "google/gemma-3-4b:2", 
        "messages": [
            {"role": "user", "content": prompt}],
        "stream": False,
        "temperature": 0.7
    }

    if audio_b64:
        data["audio"] = audio_b64
    if imagen_b64:
        data["image"] = imagen_b64

    response = requests.post(URL_CHAT, headers=HEADERS, json=data)

    if response.status_code == 200:
        try:
            return response.json()["choices"][0]["message"]["content"]
        except Exception as e:
            print("Error interpretando respuesta:", e)
            return response.text
    else:
        return f"Error {response.status_code}: {response.text}"
    
# -----------------------------------------------------------
# 1. TRADUCCIÓN DE TEXTO
# -----------------------------------------------------------
def traducirTexto():
    texto = input("Ingresa el texto a traducir: ")
    idioma = input("Ingresa el idioma destino (ej: en, fr, es): ")
    prompt = f"Traduce este texto al idioma '{idioma}': \n{texto}"
    traduccion = consultarModelo(prompt)
    print(f"\nTraducción al idioma '{idioma}':\n{traduccion}")

# -----------------------------------------------------------
# 2. DESCARGAR IMÁGENES DESDE URL
# -----------------------------------------------------------
def descargarImagen():
    url = input("URL de la imagen: ")
    nombre = input("Nombre para guardar imagen (sin formato): ")

    try:
        respuesta = requests.get(url)
        respuesta.raise_for_status()
        imagen = Image.open(BytesIO(respuesta.content))
        ruta_archivo = f"{nombre}.png"
        imagen.save(ruta_archivo)
        print(f"Imagen descargada y guardada: {ruta_archivo}")

    except Exception as e:
        print(f"Error al descargar la imagen: {e}")

# -----------------------------------------------------------
# 3. RESOLUCIÓN DE PROBLEMAS MEDIANTE IMÁGENES (EJEMPLO)
# -----------------------------------------------------------
def resolverProblemaImagen():
    ruta = input("Ingresa la ruta del archivo PNG con el problema: ")
    try:
        with open(ruta, "rb") as f:
            imagen_b64 = base64.b64encode(f.read()).decode("utf-8")
        prompt = "Extrae el problema matemático de esta imagen y resuélvelo."
        resultado = consultarModelo(prompt, imagen_b64=imagen_b64)
        print("\nResultado del modelo:\n", resultado)
    except Exception as e:
        print(f"Error al procesar la imagen: {e}")

# -----------------------------------------------------------
# 4. TRANSCRIPCIÓN DE AUDIO
# -----------------------------------------------------------
def transcribirAudio():
    ruta_audio = input("Ingresa la ruta del archivo de audio local (WAV/MP3): ")
    recognizer = sr.Recognizer()

    try:
        # Convertir MP3 a WAV si es necesario
        if ruta_audio.lower().endswith(".mp3"):
            sonido = AudioSegment.from_mp3(ruta_audio)
            ruta_wav = "temp_audio.wav"
            sonido.export(ruta_wav, format="wav")
        else:
            ruta_wav = ruta_audio

        # Abrir archivo WAV para transcripción
        with sr.AudioFile(ruta_wav) as source:
            audio_data = recognizer.record(source)

        # Transcripción
        texto = recognizer.recognize_google(audio_data, language="es-ES")
        print("\nTranscripción local del audio:\n", texto)

        # Opcional: enviar al modelo para análisis
        prompt = f"Resume o analiza el siguiente texto: {texto}"
        resultado = consultarModelo(prompt)
        print("\nAnálisis del modelo:\n", resultado)

    except FileNotFoundError:
        print(f"Error: el archivo '{ruta_audio}' no existe.")
    except sr.UnknownValueError:
        print("Error: no se pudo entender el audio.")
    except sr.RequestError as e:
        print(f"Error con el servicio de reconocimiento: {e}")
    except Exception as e:
        print(f"Error al procesar el audio: {e}")

# -----------------------------------------------------------
# MENÚ PRINCIPAL
# -----------------------------------------------------------
def menu():
    while True:
        print("\n--- ASISTENTE IA ---")
        print("1. Traducir texto")
        print("2. Descargar imagen desde URL")
        print("3. Resolver problema desde imagen PNG")
        print("4. Transcribir audio a texto")
        print("5. Salir")

        opcion = input("Selecciona una opción: ")

        if opcion == "1":
            traducirTexto()
        elif opcion == "2":
            descargarImagen()
        elif opcion == "3":
            resolverProblemaImagen()
        elif opcion == "4":
            transcribirAudio()
        elif opcion == "5":
            print("Saliendo")
            break
        else:
            print("Opción  no válida. Por favor, seleccione de nuevo")


if __name__ == "__main__":
    menu()
