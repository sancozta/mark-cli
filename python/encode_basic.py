# desc: Codifica texto em base64
import base64
import sys

if len(sys.argv) != 2:
    print('Usage: python encode_basic.py <text>')
    sys.exit(1)

print(base64.b64encode(sys.argv[1].encode('utf-8')).decode('utf-8'))