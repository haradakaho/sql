import requests

url = 'http://localhost:3000/select'
params = {
    "id" : "6"
}

res = requests.get(url, params=params)
print(res.status_code)
print(res.encoding)
print(res.json())