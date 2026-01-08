import requests

URL_MODELS = "http://192.168.0.12:1234/v1/models"
URL_CHAT = "http://192.168.0.12:1234/v1/chat/completions"

response = requests.get(URL_MODELS)

prompt_correcto = "Explica brevemente el problema con la vivienda actual en España."
prompt_erroneo = "Noze ke pAsa cn las ksas en mi pais. xq n ncuentro choza TT"

def consultarModelo(prompt):
    headers = {"Content-Type": "application/json"}

    data = {
        "model": "google/gemma-3-4b:2", 
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "stream": False,
        "temperature": 0.7
    }

    response = requests.post(URL_CHAT, headers=headers, json=data)

    if response.status_code == 200:
        try:
            return response.json()["choices"][0]["message"]["content"]
        except Exception as e:
            print("Error interpretando respuesta:", e)
            return response.text
    else:
        return f"Error {response.status_code}: {response.text}"


print("\nPROMPT CORRECTO:")
print(consultarModelo(prompt_correcto))

print("\nPROMPT ERRÓNEO:")
print(consultarModelo(prompt_erroneo))
