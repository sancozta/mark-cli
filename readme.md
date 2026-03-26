### Mark CLI

Projeto template para cli pessoal para automações via scripts Python.

#### Setup

```bash
source ./install.sh
```

Cria o venv, instala dependências e registra o comando `mark` no `.zshrc`.
Em terminais novos, reative com: `source .venv/bin/activate`

#### Uso

```bash
mark <script> [args...]
mark help       # lista scripts disponíveis
```

#### Adicionando scripts

Coloque o arquivo `.py` em `python/`. Para aparecer na listagem com descrição, adicione na primeira linha:

```python
# desc: Descrição curta do que o script faz
```

Scripts com prefixo `_` (ex: `_meu_script.py`) são tratados como privados — chamados sem o `_`:

```bash
mark meu_script
```

Módulos utilitários com prefixo `util_` **não aparecem** na listagem e não são executados diretamente.

#### Scripts incluídos

| Script         | Descrição                                       |
| -------------- | ----------------------------------------------- |
| `decode_basic` | Decodifica token base64                         |
| `decode_jwt`   | Decodifica token JWT (sem verificar assinatura) |
| `encode_basic` | Codifica texto em base64                        |
| `get_screen`   | Captura screenshot de uma URL                   |

```bash
mark decode_basic <base64_token>
mark decode_jwt <jwt_token>
mark encode_basic <texto>
mark get_screen <url>
```
