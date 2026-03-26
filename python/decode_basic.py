# desc: Decodifica token base64
import base64
import sys

if len(sys.argv) != 2:
    print('Usage: python decode_basic.py <base64_token>')
    sys.exit(1)

print(base64.b64decode(sys.argv[1]).decode('utf-8'))