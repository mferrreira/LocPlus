import urllib.request
import urllib.parse
import json
import ssl

base = "http://127.0.0.1:8000"
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

def post(url, payload, token=None):
    req = urllib.request.Request(base + url, method="POST")
    req.add_header('Content-Type', 'application/json')
    if token:
        req.add_header('Authorization', f'Bearer {token}')
    try:
        res = urllib.request.urlopen(req, data=json.dumps(payload).encode('utf-8'), context=ctx)
        raw = res.read()
        try:
            return res.status, json.loads(raw)
        except:
            return res.status, raw.decode()
    except urllib.error.HTTPError as e:
        raw = e.read()
        try:
            return e.code, json.loads(raw)
        except:
            return e.code, raw.decode()

def get(url, token=None):
    req = urllib.request.Request(base + url, method="GET")
    if token:
        req.add_header('Authorization', f'Bearer {token}')
    try:
        res = urllib.request.urlopen(req, context=ctx)
        raw = res.read()
        try:
            return res.status, json.loads(raw)
        except:
            return res.status, raw.decode()
    except urllib.error.HTTPError as e:
        raw = e.read()
        try:
            return e.code, json.loads(raw)
        except:
            return e.code, raw.decode()

print("=== STARTING LOCPLUS V2 API QA ===")

# 1. Health
s, d = get("/")
print(f"1. [HealthCheck]: {s}")

# 2. Cadastro PJ
payload_pj = {
    "nome_completo": "Imperador das Máquinas QA",
    "email": "qa_imperador@test.com",
    "senha": "123456",
    "objetivo": "disponibilizar_maquinas",
    "tipo_entidade": "pessoa_juridica",
    "documento": "12345678000199",
    "telefone_celular": "11999999999",
    "razao_social": "Mquinas QA LTDA",
    "nome_fantasia": "MaqQA",
    "inscricao_estadual": "ISENTO"
}
s, data = post("/usuarios/cadastro", payload_pj)
print(f"2. [Cadastro PJ]: {s} -> {str(data)[:100]}")

# 3. Login
s, data = post("/usuarios/login", {"email": "qa_imperador@test.com", "senha": "123456"})
print(f"3. [Login]: {s}")
token = data.get('access_token') if s == 200 else None
if not token:
    print(f"   ! Falha ao resgatar token: {data}")

if token:
    # 4. Criar Endereço
    payload_end = {
        "cep": "01000-000", "logradouro": "Rua XYZ QA", 
        "numero": "123", "bairro": "Centro", "cidade": "São Paulo", 
        "estado": "SP", "tipo": "sede", "is_padrao": True
    }
    s, data = post("/enderecos/", payload_end, token)
    print(f"4. [Criar Endereço]: {s} -> {str(data)[:100]}")

    # 5. Listar Equipamentos
    s, data = get("/equipamentos/")
    print(f"5. [Vitrine]: {s} -> Listou {len(data) if type(data) is list else data} máquinas.")

print("=== FINISHED ===")
