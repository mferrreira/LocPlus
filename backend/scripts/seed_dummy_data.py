import sys
import os

# Adiciona a raiz do backend ao path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.core.database import SessionLocal
from app.models.usuarios import Usuario, ObjetivoConta, TipoEntidade
from app.models.empresas import Empresa
from app.models.clientes import Cliente
from app.models.equipamentos import Equipamento, CategoriaEquipamento
from app.models.enderecos import Endereco
from app.models.documentos_kyc import DocumentoKYC
from app.models.representacao_b2b import RepresentacaoB2B
from app.core.security import get_password_hash

def seed():
    db = SessionLocal()
    
    if db.query(Usuario).count() > 0:
        print("Banco já possui dados! Limpe-o se quiser resetar.")
        db.close()
        return

    print("🌱 Iniciando plantio de Dummy Data...")

    # 1. Usuário Locador (Empresa)
    locador_user = Usuario(
        nome_completo="João da LocPlus",
        email="joao@locador.com",
        senha_hash=get_password_hash("senha123"),
        objetivo=ObjetivoConta.LOCADOR,
        tipo_entidade=TipoEntidade.PJ,
        documento="11.222.333/0001-44",
        telefone_celular="11999998888",
        razao_social="LocPlus Equipamentos Ltda",
        nome_fantasia="LocPlus"
    )
    db.add(locador_user)
    db.commit()
    db.refresh(locador_user)
    
    empresa = Empresa(usuario_id=locador_user.id)
    db.add(empresa)
    db.commit()
    db.refresh(empresa)

    # 2. Usuário Locatário (Cliente PF)
    cliente_user = Usuario(
        nome_completo="Carlos Construtor",
        email="carlos@cliente.com",
        senha_hash=get_password_hash("senha123"),
        objetivo=ObjetivoConta.LOCATARIO,
        tipo_entidade=TipoEntidade.PF,
        documento="123.456.789-00",
        telefone_celular="11977776666",
        rg="MG-11.222.333",
    )
    db.add(cliente_user)
    db.commit()
    db.refresh(cliente_user)
    
    cliente = Cliente(usuario_id=cliente_user.id)
    db.add(cliente)
    db.commit()

    # 3. Equipamentos Cativantes com imagens realistas de Unsplash
    equipamentos = [
        Equipamento(
            nome="Retroescavadeira Caterpillar 416F2",
            descricao="Máquina robusta e bruta ideal para terraplanagem, escavação e elevação de cargas pesadas nas obras brutas.",
            numero_serie_patrimonio="CAT-416-001",
            marca="Caterpillar", modelo="416F2", ano_fabricacao=2020,
            valor_diaria=850.00, valor_semana=5000.00, valor_quinzena=9000.00, valor_mes=15000.00,
            foto_visao_geral="https://images.unsplash.com/photo-1582213782179-e0d53f98f2ca?q=80&w=600&auto=format&fit=crop",
            categoria=CategoriaEquipamento.LINHA_PESADA,
            quantidade_total=2, quantidade_disponivel=2,
            empresa_id=empresa.id
        ),
        Equipamento(
            nome="Trator Agrícola John Deere D130",
            descricao="Trator forte para campos abertos, chácaras de alta rodagem e agronegócio que demanda tecnologia e conforto.",
            numero_serie_patrimonio="JD-D130-99",
            marca="John Deere", modelo="D130", ano_fabricacao=2019,
            valor_diaria=300.00, valor_semana=1800.00, valor_mes=5000.00,
            foto_visao_geral="https://images.unsplash.com/photo-1616450654122-25de12bc4434?q=80&w=600&auto=format&fit=crop",
            categoria=CategoriaEquipamento.LINHA_LEVE,
            quantidade_total=1, quantidade_disponivel=0, # Simulando estar alugado!
            empresa_id=empresa.id
        ),
        Equipamento(
            nome="Caminhão Munck VW 8.160",
            descricao="Caminhão de guindaste veicular forte e ágil para içamento de containers e materiais estruturais das indústrias.",
            numero_serie_patrimonio="VW-8160-55",
            marca="Volkswagen", modelo="8.160", ano_fabricacao=2022,
            valor_diaria=1200.00, valor_semana=7000.00, valor_mes=22000.00,
            foto_visao_geral="https://images.unsplash.com/photo-1616683696541-11b05ff9ea27?q=80&w=600&auto=format&fit=crop",
            categoria=CategoriaEquipamento.VEICULOS,
            quantidade_total=1, quantidade_disponivel=1,
            empresa_id=empresa.id
        ),
        Equipamento(
            nome="Betoneira 400L Elétrica CSM",
            descricao="O clássico do pedreiro autônomo. Betoneira de 400 Litros com motor elétrico 2CV 220V que faz 1 saco bruto e cimento.",
            numero_serie_patrimonio=None, 
            marca="CSM", modelo="400L", ano_fabricacao=2023,
            valor_diaria=85.00, valor_semana=400.00, valor_mes=1200.00,
            foto_visao_geral="https://images.unsplash.com/photo-1541888086-218eb8a37943?q=80&w=600&auto=format&fit=crop",
            categoria=CategoriaEquipamento.LINHA_LEVE,
            quantidade_total=10, quantidade_disponivel=8,
            empresa_id=empresa.id
        ),
        Equipamento(
            nome="Container Padrão 20 Pés (Refeitório)",
            descricao="Módulo Dry de aço com isolamento termo-acústico ideal para instalação de almoxarifados blindados e refeitórios rápidos na obra.",
            numero_serie_patrimonio="CONT-20-A",
            marca="DryVan", modelo="20 Pés", ano_fabricacao=2015,
            valor_diaria=150.00, valor_mes=800.00,
            foto_visao_geral="https://images.unsplash.com/photo-1494412574643-ff11b0a5c1c3?q=80&w=600&auto=format&fit=crop",
            categoria=CategoriaEquipamento.MENSALISTAS,
            quantidade_total=5, quantidade_disponivel=5,
            empresa_id=empresa.id
        ),
        Equipamento(
            nome="Martelo Rompedor 30Kg Makita",
            descricao="Para quebrar asfalto, destruir vigas armadas ou lajes grossas sem dor de cabeça no ombro e punho! Baita absorção.",
            numero_serie_patrimonio="MAK-30-X",
            marca="Makita", modelo="HM1810", ano_fabricacao=2021,
            valor_diaria=120.00, valor_semana=600.00, valor_mes=1800.00,
            foto_visao_geral="https://images.unsplash.com/photo-1504917595217-d4dc5ebe6122?q=80&w=600&auto=format&fit=crop",
            categoria=CategoriaEquipamento.DIVERSOS,
            quantidade_total=4, quantidade_disponivel=3,
            empresa_id=empresa.id
        )
    ]
    
    db.add_all(equipamentos)
    db.commit()
    print("✅ Dummy Data Injetada: 2 Usuários e 6 Máquinas Pesadas adicionadas ao banco de dados!")
    db.close()

if __name__ == "__main__":
    seed()
