# test.py
import requests

# Datos
LOGIN_URL = "http://localhost:8080/login"
DELETE_URL = "http://localhost:8081/delete-publication"

# 1. Login
login_data = {
    "User_mail": "ascorread",  # Asegúrate de que exista
    "password": "1234"
}
login_response = requests.post(LOGIN_URL, json=login_data)

if login_response.status_code != 200:
    print("Login failed:", login_response.status_code, login_response.text)
    exit()

token = login_response.json().get("token")
print("Token:", token)

# 2. Enviar la solicitud de eliminación
headers = {
    "Authorization": f"Bearer {token}"
}

# Asegúrate de reemplazar esto con un ObjectId válido de MongoDB
publication_id = "68574f986e9721e3b7666d2f"  # <-- cambia por una válida

payload = {
    "publication_id": publication_id
}

response = requests.put(DELETE_URL, json=payload, headers=headers)

print("Status Code:", response.status_code)
print("Response:", response.json())
