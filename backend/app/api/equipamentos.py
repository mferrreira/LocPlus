from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

# Importações da nossa arquitetura
from app.core.database import get_db
from app.models.equipamentos import Equipamento
from app.models.usuarios import Empresa
from app.schemas.equipamentos import EquipamentoCreate, EquipamentoResponse

# Roteador dedicado ao Estoque
router = APIRouter(prefix="/equipamentos", tags=["Estoque e Máquinas"])

# ==========================================
# CADASTRAR NOVO EQUIPAMENTO (POST)
# ==========================================
@router.post("/", response_model=EquipamentoResponse, status_code=status.HTTP_201_CREATED)
def cadastrar_equipamento(equipamento: EquipamentoCreate, db: Session = Depends(get_db)):
    
    # Validação de Chave Estrangeira: A empresa informada realmente existe?
    empresa_dona = db.query(Empresa).filter(Empresa.id == equipamento.empresa_id).first()
    if not empresa_dona:
        raise HTTPException(status_code=404, detail="A Empresa (Locadora) informada não existe no sistema.")
        
    # Regra: Se o item tiver um número de série, ele não pode ser duplicado
    if equipamento.numero_serie_patrimonio:
        serie_existente = db.query(Equipamento).filter(Equipamento.numero_serie_patrimonio == equipamento.numero_serie_patrimonio).first()
        if serie_existente:
            raise HTTPException(status_code=400, detail="Este Número de Série/Patrimônio já está cadastrado.")

    # Converte o Schema para o Modelo do Banco
    novo_equipamento = Equipamento(
        nome=equipamento.nome,
        descricao=equipamento.descricao,
        numero_serie_patrimonio=equipamento.numero_serie_patrimonio,
        valor_base_locacao=equipamento.valor_base_locacao,
        tipo_cobranca=equipamento.tipo_cobranca,
        categoria=equipamento.categoria,
        quantidade_total=equipamento.quantidade_total,
        quantidade_disponivel=equipamento.quantidade_total, # Na hora da compra, tudo está disponível
        empresa_id=equipamento.empresa_id
    )

    # Gravação física no banco de dados
    db.add(novo_equipamento)
    db.commit()
    db.refresh(novo_equipamento)

    return novo_equipamento

# ==========================================
# LISTAR ESTOQUE (GET)
# ==========================================
@router.get("/", response_model=List[EquipamentoResponse])
def listar_equipamentos(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    # Busca paginada para performance em grandes estoques
    return db.query(Equipamento).offset(skip).limit(limit).all()