from fastapi.testclient import TestClient
from datetime import datetime
import json
import uuid

# Assume a estrutura root do backend
from app.main import app

client = TestClient(app)

def test_full_business_cycle():
    # 1. CRIAÇÃO DE LOCADOR E VALIDAÇÃO DE FREEMIUM TRIAL
    # Geramos documentação fake para não conflitar com banco real
    fake_cnpj = str(uuid.uuid4())[:14]
    fake_email = f"locadora_{fake_cnpj}@teste.com"
    
    payload_cadastro = {
        "email": fake_email,
        "objetivo": "disponibilizar_maquinas",
        "tipo_entidade": "pessoa_juridica",
        "nome_completo": "Locadora Teste TDD",
        "documento": fake_cnpj,
        "razao_social": "Locadora Teste Ltda",
        "nome_fantasia": "Locadora Teste",
        "inscricao_estadual": "123456789",
        "senha": "password123",
        "viu_guia_cadastro": True
    }
    
    response_cadastro = client.post("/usuarios/cadastro", json=payload_cadastro)
    assert response_cadastro.status_code == 201, f"Erro Cadastro: {response_cadastro.json()}"
    
    # Faz login para extrair tokens
    response_login = client.post("/usuarios/login", data={"username": fake_email, "password": "password123"})
    assert response_login.status_code == 200, f"Erro Login: {response_login.json()}"
    tokens = response_login.json()
    access_token = tokens["access_token"]
    refresh_token = tokens["refresh_token"]
    
    # 2. VALIDAÇÃO DO REFRESH TOKEN
    response_refresh = client.post("/usuarios/refresh", json={"refresh_token": refresh_token})
    assert response_refresh.status_code == 200, f"Erro Refresh: {response_refresh.json()}"
    new_access_token = response_refresh.json()["access_token"]
    
    headers = {"Authorization": f"Bearer {new_access_token}"}
    
    # Pré-requisito: Criar categoria para a máquina (ignora se houver mock, mas as rotas requerem o enum string)
    categoria_padrao = "linha_pesada" 
    
    # 3. VALIDAÇÃO DE LIMITES DE ASSINATURA (Max Máquinas: 3 no Freemium)
    # Vamos cadastrar 3 máquinas com sucesso
    ids_maquinas = []
    
    for i in range(3):
        payload_maquina = {
            "nome": f"Máquina {i}",
            "valor_diaria": 150.0,
            "categoria": categoria_padrao,
            "quantidade_total": 1,
            "empresa_id": 0 # Fake value, should be overwritten by injection
        }
        resp_maq = client.post("/equipamentos/", json=payload_maquina, headers=headers)
        assert resp_maq.status_code == 201, f"Erro cadastro de máquina {i}: {resp_maq.json()}"
        ids_maquinas.append(resp_maq.json()["id"])
        
    # A 4ª Máquina PRECISA quebrar
    payload_maquina_4 = {
        "nome": "Máquina 4 - Bloqueada",
        "valor_diaria": 200.0,
        "categoria": categoria_padrao,
        "quantidade_total": 1,
        "empresa_id": 0
    }
    resp_break = client.post("/equipamentos/", json=payload_maquina_4, headers=headers)
    assert resp_break.status_code == 403, f"Erro de Limite não funcionou! Status retornado: {resp_break.status_code}"
    
    # 4. VALIDAÇÃO DO MOTOR DE CONTRATOS E MATEMÁTICA DE DIAS
    # Criação de um Cliente fake para ser o locatário do contrato
    fake_cpf = str(uuid.uuid4())[:11]
    cliente_payload = {
        "email": f"locatario_{fake_cpf}@teste.com",
        "objetivo": "alugar_maquinas",
        "tipo_entidade": "pessoa_fisica",
        "nome_completo": "Locatário Teste TDD",
        "documento": fake_cpf,
        "rg": "1234567",
        "data_nascimento": "1990-01-01",
        "senha": "password123",
        "viu_guia_cadastro": True
    }
    resp_cli = client.post("/usuarios/cadastro", json=cliente_payload)
    assert resp_cli.status_code == 201, f"Erro cadastro cliente: {resp_cli.json()}"
    usuario_cliente_id = resp_cli.json()["id"]
    
    # Pega o ID real da tabela Cliente
    from app.core.database import SessionLocal
    from app.models.clientes import Cliente
    db_session = SessionLocal()
    perfil_cliente = db_session.query(Cliente).filter(Cliente.usuario_id == usuario_cliente_id).first()
    cliente_db_id = perfil_cliente.id
    db_session.close()
    
    # Cria a locação de MESMO DIA
    hoje = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S.000Z")
    locacao_payload = {
         "empresa_id": 0, 
         "cliente_id": cliente_db_id,
         "equipamento_id": ids_maquinas[0],
         "data_inicio": hoje,
         "data_fim_prevista": hoje,
         "status": "em_andamento" # Já engatilha remoção do estoque
    }
    
    resp_loc = client.post("/locacoes/", json=locacao_payload, headers=headers)
    assert resp_loc.status_code == 201, f"Erro Geração de Contrato: {resp_loc.json()}"
    contrato = resp_loc.json()
    
    # Asserções Matemáticas
    assert contrato["valor_total"] == 150.0, f"Valor total inválido: {contrato['valor_total']}. Deveria ser 1 diária de 150."
    
    # Consulta a máquina 1 para ver se o estoque desceu (Era 1, deve virar 0)
    # A vitrine do catalogo é aberta
    resp_catalogo = client.get(f"/catalogo/maquinas")
    vitrine = resp_catalogo.json()
    
    maquina_testada = next(m for m in vitrine if m["id"] == ids_maquinas[0])
    assert maquina_testada["quantidade_disponivel"] == 0, "Estoque do equipamento não foi subitamente deduzido!"
    
    print("\n✅ TDD PASSED! Pipeline Core Integrado Validado!")

if __name__ == "__main__":
    test_full_business_cycle()
