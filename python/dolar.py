# desc: Cotação atual do dólar (USD → BRL)
import requests

try:
    resp = requests.get('https://economia.awesomeapi.com.br/last/USD-BRL', timeout=10)
    data = resp.json()['USDBRL']

    print(f'  Dólar (USD → BRL)\n')
    print(f'  Compra:    R$ {float(data["bid"]):.4f}')
    print(f'  Venda:     R$ {float(data["ask"]):.4f}')
    print(f'  Máxima:    R$ {float(data["high"]):.4f}')
    print(f'  Mínima:    R$ {float(data["low"]):.4f}')
    print(f'  Variação:  {data["varBid"]} ({data["pctChange"]}%)')
    print(f'  Atualizado: {data["create_date"]}')
except Exception as e:
    print(f'  Erro ao consultar cotação: {e}')
