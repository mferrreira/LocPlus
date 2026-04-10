from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import datetime

# Importações da nossa arquitetura
from app.core.database import get_db
from app.models.locacoes import Locacao, StatusLocacao
from app.models.equipamentos import Equipamento
from app.models.clientes import Cliente
from app.api.deps import get_current_tenant
from app.models.empresas import Empresa
from app.schemas.locacoes import LocacaoCreate, LocacaoResponse

# Roteador dedicado à Operação
router = APIRouter(prefix="/locacoes", tags=["Operacional (Locações e Contratos)"])

# ==========================================
# CRIAR NOVO CONTRATO/ORÇAMENTO (POST)
# ==========================================
@router.post("/", response_model=LocacaoResponse, status_code=status.HTTP_201_CREATED)
def criar_locacao(
    locacao: LocacaoCreate, 
    db: Session = Depends(get_db),
    current_tenant: Empresa = Depends(get_current_tenant)
):
    # 2. Trava de Segurança: O Cliente existe?
    cliente = db.query(Cliente).filter(Cliente.id == locacao.cliente_id).first()
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente (Locatário) não encontrado no banco de dados.")

    # 3. Trava de Segurança Logística: A Máquina existe, tem estoque e PERTENCE ao Tenant?
    equipamento = db.query(Equipamento).filter(
        Equipamento.id == locacao.equipamento_id,
        Equipamento.empresa_id == current_tenant.id
    ).first()
    
    if not equipamento:
        raise HTTPException(status_code=404, detail="Equipamento não encontrado no estoque desta Locadora.")
    
    if equipamento.quantidade_disponivel <= 0:
        raise HTTPException(status_code=400, detail="Este equipamento não possui unidades disponíveis para locação no momento.")

    import math
    
    # 4. Cálculo do Motor de Aluguel
    # Previne fusos conflitantes
    data_fim = locacao.data_fim_prevista.replace(tzinfo=None)
    data_inicio = locacao.data_inicio.replace(tzinfo=None) if locacao.data_inicio else datetime.utcnow()
    
    # Regra de Negócio Física: 0 dias = 1 diária mínima
    diferenca = (data_fim - data_inicio).days
    dias_cobrados = max(1, math.ceil(diferenca))
    
    valor_total_calculado = dias_cobrados * equipamento.valor_diaria

    # 5. Prepara a gravação do Contrato
    nova_locacao = Locacao(
        empresa_id=current_tenant.id, # O Tenant injetado previne fraudes de payload
        cliente_id=locacao.cliente_id,
        equipamento_id=locacao.equipamento_id,
        data_inicio=data_inicio,
        data_fim_prevista=data_fim,
        valor_total=valor_total_calculado,
        endereco_entrega=locacao.endereco_entrega,
        aluguel_representacao=locacao.aluguel_representacao,
        status=locacao.status
    )

    # 6. O Gatilho de Estoque: Se o contrato já nascer "Em Andamento", tira 1 do estoque
    if nova_locacao.status in [StatusLocacao.EM_ANDAMENTO, StatusLocacao.ORCAMENTO]:
        equipamento.quantidade_disponivel -= 1

    # 6. Executa a transação no PostgreSQL
    db.add(nova_locacao)
    db.commit()
    db.refresh(nova_locacao)

    return nova_locacao

# ==========================================
# MÁQUINA DE ESTADOS: ACEITE DO LOCATÁRIO
# ==========================================
@router.post("/{locacao_id}/aceite")
def aceite_locatario(
    locacao_id: int, 
    db: Session = Depends(get_db),
    current_tenant: Empresa = Depends(get_current_tenant)
):
    locacao = db.query(Locacao).filter(
        Locacao.id == locacao_id,
        Locacao.empresa_id == current_tenant.id
    ).first()
    if not locacao:
        raise HTTPException(status_code=404, detail="Contrato não encontrado")
        
    locacao.status = StatusLocacao.EM_ANDAMENTO
    locacao.data_aceite_locatario = datetime.utcnow()
    db.commit()
    return {"mensagem": "Aceite digital assinado. Máquina oficialmente com o locatário."}

# ==========================================
# MÁQUINA DE ESTADOS: MÁQUINA PARADA (S.O.S)
# ==========================================
@router.post("/{locacao_id}/maquina-parada")
def reportar_maquina_parada(
    locacao_id: int, 
    db: Session = Depends(get_db),
    current_tenant: Empresa = Depends(get_current_tenant)
):
    locacao = db.query(Locacao).filter(
        Locacao.id == locacao_id,
        Locacao.empresa_id == current_tenant.id
    ).first()
    if not locacao:
        raise HTTPException(status_code=404, detail="Contrato não encontrado")
        
    locacao.status = StatusLocacao.MAQUINA_PARADA
    # Todo o calculo financeiro de quebra de diária acontecerá com base nesse status no futuro
    db.commit()
    return {"mensagem": "Assistência notificada. Contagem de diárias pausada pelo sistema."}

# ==========================================
# LISTAR CONTRATOS E ORÇAMENTOS (GET)
# ==========================================
@router.get("/", response_model=List[LocacaoResponse])
def listar_locacoes(
    skip: int = 0, 
    limit: int = 100, 
    db: Session = Depends(get_db),
    current_tenant: Empresa = Depends(get_current_tenant)
):
    return db.query(Locacao).filter(Locacao.empresa_id == current_tenant.id).offset(skip).limit(limit).all()

from app.core.security import get_current_user
from app.models.usuarios import Usuario

# ==========================================
# LISTAR MINHAS LOCAÇÕES ATIVAS (LOCATÁRIO) (GET)
# ==========================================
@router.get("/meus", response_model=List[LocacaoResponse])
def listar_minhas_locacoes(
    skip: int = 0, 
    limit: int = 100, 
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    # Pega o id do perfil de cliente desse usuário
    cliente_id = current_user.perfil_cliente[0].id if current_user.perfil_cliente else None
    
    if not cliente_id:
        raise HTTPException(status_code=403, detail="Sua conta não possui um Perfil Locatário vinculado.")
        
    return db.query(Locacao).filter(Locacao.cliente_id == cliente_id).offset(skip).limit(limit).all()
