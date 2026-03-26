# desc: Decodifica token JWT (sem verificar assinatura)
import json
import sys

import jwt

if len(sys.argv) != 2:
    print('Usage: python decode_jwt.py <jwt_token>')
    sys.exit(1)

token = sys.argv[1]
decoded = jwt.decode(token, options={'verify_signature': False})
print(json.dumps(decoded, indent=4))