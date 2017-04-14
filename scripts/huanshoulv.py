import requests

r = requests.get('https://server.huanshoulv.com:443')

print(r.status_code)
print(r.text)
