from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

# Importações da nossa arquitetura
from app.core.database import get_db
from app.models.locacoes import Locacao, StatusLocacao
from app.models.equipamentos import Equipamento
from app.models.usuarios import Cliente, Empresa
from app.schemas.locacoes import LocacaoCreate, LocacaoResponse

# Roteador dedicado à Operação
router = APIRouter(prefix="/locacoes", tags=["Operacional (Locações e Contratos)"])

# ==========================================
# CRIAR NOVO CONTRATO/ORÇAMENTO (POST)
# ==========================================
@router.post("/", response_model=LocacaoResponse, status_code=status.HTTP_201_CREATED)
def criar_locacao(locacao: LocacaoCreate, db: Session = Depends(get_db)):
    
    # 1. Trava de Segurança: A Locadora existe?
    empresa = db.query(Empresa).filter(Empresa.id == locacao.empresa_id).first()
    if not empresa:
        raise HTTPException(status_code=404, detail="Empresa (Locadora) não encontrada no banco de dados.")

    # 2. Trava de Segurança: O Cliente existe?
    cliente = db.query(Cliente).filter(Cliente.id == locacao.cliente_id).first()
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente (Locatário) não encontrado no banco de dados.")

    # 3. Trava de Segurança Logística: A Máquina existe e tem estoque?
    equipamento = db.query(Equipamento).filter(Equipamento.id == locacao.equipamento_id).first()
    if not equipamento:
        raise HTTPException(status_code=404, detail="Equipamento não encontrado no estoque.")
    
    if equipamento.quantidade_disponivel <= 0:
        raise HTTPException(status_code=400, detail="Este equipamento não possui unidades disponíveis para locação no momento.")

    # 4. Prepara a gravação do Contrato
    nova_locacao = Locacao(
        empresa_id=locacao.empresa_id,
        cliente_id=locacao.cliente_id,
        equipamento_id=locacao.equipamento_id,
        data_fim_prevista=locacao.data_fim_prevista.replace(tzinfo=None), # Remove fuso horário conflitante
        valor_total=locacao.valor_total,
        endereco_entrega=locacao.endereco_entrega,
        aluguel_representacao=locacao.aluguel_representacao,
        status=locacao.status
    )

    # 5. O Gatilho de Estoque: Se o contrato já nascer "Em Andamento", tira 1 do estoque
    if nova_locacao.status == StatusLocacao.EM_ANDAMENTO:
        equipamento.quantidade_disponivel -= 1

    # 6. Executa a transação no PostgreSQL
    db.add(nova_locacao)
    db.commit()
    db.refresh(nova_locacao)

    return nova_locacao

# ==========================================
# LISTAR CONTRATOS E ORÇAMENTOS (GET)
# ==========================================
@router.get("/", response_model=List[LocacaoResponse])
def listar_locacoes(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    # Retorna o fluxo de caixa/operações
    return db.query(Locacao).offset(skip).limit(limit).all()