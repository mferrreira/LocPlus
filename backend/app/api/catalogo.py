from typing import List, Optional
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import or_

from app.core.database import get_db
from app.models.equipamentos import Equipamento, CategoriaEquipamento
from app.schemas.equipamentos import CatalogoEquipamentoResponse

# Roteador dedicado ao Público Global
router = APIRouter(prefix="/catalogo", tags=["Marketplace (Vitrine Pública)"])

@router.get("/maquinas", response_model=List[CatalogoEquipamentoResponse])
def listar_catalogo_maquinas(
    q: Optional[str] = Query(None, description="Termo de busca para título, marca ou modelo"),
    categoria_id: Optional[CategoriaEquipamento] = Query(None, description="Filtrar por Categoria"),
    preco_maximo: Optional[float] = Query(None, description="Valor máximo da diária"),
    apenas_disponiveis: bool = Query(False, description="Oculta máquinas que estão zeradas no estoque"),
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    # 1. Base Query com JoinedLoad (Eager Loading para performance 1+N)
    # Traz a Empresa proprietária em uma única viagem ao banco de dados.
    query = db.query(Equipamento).options(joinedload(Equipamento.empresa))
    
    # 2. Busca Textual Híbrida
    if q:
        termo = f"%{q}%"
        query = query.filter(
            or_(
                Equipamento.nome.ilike(termo),
                Equipamento.marca.ilike(termo),
                Equipamento.modelo.ilike(termo),
                Equipamento.descricao.ilike(termo)
            )
        )
        
    # 3. Filtros Estritos B2B
    if categoria_id:
        query = query.filter(Equipamento.categoria == categoria_id)
        
    if preco_maximo is not None:
        query = query.filter(Equipamento.valor_diaria <= preco_maximo)
        
    # 4. A Regra de Estoque (Marketplace visibility logic)
    if apenas_disponiveis:
        query = query.filter(Equipamento.quantidade_disponivel > 0)
        
    # 5. Ordenação: por padrão os mais baratos ou recém inseridos. 
    # Podemos incrementar no futuro. Usaremos .id desc por consistência.
    query = query.order_by(Equipamento.id.desc())

    # 6. Executa a paginação e resolve
    return query.offset(skip).limit(limit).all()
