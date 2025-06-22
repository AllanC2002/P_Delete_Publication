import requests

LOGIN_URL = "http://localhost:8080/login"
DELETE_URL = "http://localhost:8081/delete-publication"


login_data = {
    "User_mail": "ascorread", 
    "password": "1234"
}
login_response = requests.post(LOGIN_URL, json=login_data)

if login_response.status_code != 200:
    print("Login failed:", login_response.status_code, login_response.text)
    exit()

token = login_response.json().get("token")
print("Token:", token)

headers = {
    "Authorization": f"Bearer {token}"
}

publication_id = "68587f8b5dfa12355fab95b4"  

payload = {
    "publication_id": publication_id
}

response = requests.put(DELETE_URL, json=payload, headers=headers)

print("Status Code:", response.status_code)
print("Response:", response.json())
