# desc: Mostra IP público e local
import socket
import requests

try:
    public = requests.get('https://api.ipify.org', timeout=5).text
except Exception:
    public = 'não disponível'

try:
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(('8.8.8.8', 80))
    local = s.getsockname()[0]
    s.close()
except Exception:
    local = 'não disponível'

print(f'  Público:  {public}')
print(f'  Local:    {local}')
