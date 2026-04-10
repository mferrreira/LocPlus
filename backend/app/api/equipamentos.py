from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Query
from app.core.storage import upload_file_to_minio
from sqlalchemy.orm import Session
from sqlalchemy import or_, asc, desc
from app.models.equipamentos import CategoriaEquipamento

# Importações da nossa arquitetura
from app.core.database import get_db
from app.models.equipamentos import Equipamento
from app.models.empresas import Empresa
from app.api.deps import get_current_tenant, verificar_limite_maquinas
from app.schemas.equipamentos import EquipamentoCreate, EquipamentoResponse

# Roteador dedicado ao Estoque
router = APIRouter(prefix="/equipamentos", tags=["Estoque e Máquinas"])

# ==========================================
# CADASTRAR NOVO EQUIPAMENTO (POST)
# ==========================================
@router.post("/", response_model=EquipamentoResponse, status_code=status.HTTP_201_CREATED)
def cadastrar_equipamento(
    equipamento: EquipamentoCreate, 
    db: Session = Depends(get_db),
    current_tenant: Empresa = Depends(get_current_tenant),
    limite_valido: bool = Depends(verificar_limite_maquinas)
):
    # Regra: Se o item tiver um número de série, ele não pode ser duplicado dentro da locadora
    if equipamento.numero_serie_patrimonio:
        serie_existente = db.query(Equipamento).filter(
            Equipamento.numero_serie_patrimonio == equipamento.numero_serie_patrimonio,
            Equipamento.empresa_id == current_tenant.id
        ).first()
        if serie_existente:
            raise HTTPException(status_code=400, detail="Este Número de Série/Patrimônio já está cadastrado na sua frota.")

    # Converte o Schema para o Modelo do Banco
    novo_equipamento = Equipamento(
        nome=equipamento.nome,
        descricao=equipamento.descricao,
        numero_serie_patrimonio=equipamento.numero_serie_patrimonio,
        marca=equipamento.marca,
        modelo=equipamento.modelo,
        ano_fabricacao=equipamento.ano_fabricacao,
        valor_diaria=equipamento.valor_diaria,
        valor_semana=equipamento.valor_semana,
        valor_quinzena=equipamento.valor_quinzena,
        valor_mes=equipamento.valor_mes,
        foto_visao_geral=equipamento.foto_visao_geral,
        foto_painel=equipamento.foto_painel,
        foto_motor=equipamento.foto_motor,
        categoria=equipamento.categoria,
        quantidade_total=equipamento.quantidade_total,
        quantidade_disponivel=equipamento.quantidade_total,
        empresa_id=current_tenant.id # Override: Ignora o payload e usa o Contexto Seguro
    )

    db.add(novo_equipamento)
    db.commit()
    db.refresh(novo_equipamento)

    return novo_equipamento

# ==========================================
# UPLOAD DE FOTOS PARA O MINIO (POST)
# ==========================================
@router.post("/{equipamento_id}/fotos", response_model=EquipamentoResponse)
def upload_fotos_equipamento(
    equipamento_id: int, 
    tipo_foto: str, # 'visao_geral', 'painel', 'motor'
    file: UploadFile = File(...), 
    db: Session = Depends(get_db),
    current_tenant: Empresa = Depends(get_current_tenant)
):
    equipamento = db.query(Equipamento).filter(
        Equipamento.id == equipamento_id, 
        Equipamento.empresa_id == current_tenant.id
    ).first()
    if not equipamento:
        raise HTTPException(status_code=404, detail="Equipamento não encontrado")
        
    # Gera o nome de arquivo seguro pro S3 incluindo tenant_id para segregação estrutural
    nome_arquivo = f"{current_tenant.id}/equipamentos/{equipamento_id}_{tipo_foto}_{file.filename}"
    
    # Envia pro bucket MinIO
    s3_url = upload_file_to_minio(file, nome_arquivo)
    
    # Atualiza a string na tabela correta
    if tipo_foto == 'visao_geral':
        equipamento.foto_visao_geral = s3_url
    elif tipo_foto == 'painel':
        equipamento.foto_painel = s3_url
    elif tipo_foto == 'motor':
        equipamento.foto_motor = s3_url
    else:
        raise HTTPException(status_code=400, detail="tipo_foto deve ser 'visao_geral', 'painel' ou 'motor'")
        
    db.commit()
    db.refresh(equipamento)
    
    return equipamento

# ==========================================
# LISTAR ESTOQUE AVANÇADO E FILTROS (GET)
# ==========================================
@router.get("/{equipamento_id}", response_model=EquipamentoResponse)
def buscar_equipamento(
    equipamento_id: int, 
    db: Session = Depends(get_db),
    current_tenant: Empresa = Depends(get_current_tenant)
):
    eq = db.query(Equipamento).filter(
        Equipamento.id == equipamento_id,
        Equipamento.empresa_id == current_tenant.id
    ).first()
    if not eq:
        raise HTTPException(status_code=404, detail="Máquina inativa ou não encontrada.")
    return eq

@router.get("/", response_model=List[EquipamentoResponse])
def listar_equipamentos(
    busca: Optional[str] = Query(None, description="Busca por nome, marca ou modelo"),
    categoria: Optional[CategoriaEquipamento] = None,
    preco_min: Optional[float] = None,
    preco_max: Optional[float] = None,
    ordenar_por: Optional[str] = Query(None, description="'menor_preco' ou 'maior_preco'"),
    skip: int = 0, 
    limit: int = 100, 
    db: Session = Depends(get_db),
    current_tenant: Empresa = Depends(get_current_tenant)
):
    # 1. Inicia a Factory de Query do SQLAlchemy escopada ao Tenant
    query = db.query(Equipamento).filter(Equipamento.empresa_id == current_tenant.id)
    
    # 2. Busca Híbrida (Passo 6.1)
    if busca:
        termo = f"%{busca}%"
        query = query.filter(
            or_(
                Equipamento.nome.ilike(termo),
                Equipamento.marca.ilike(termo),
                Equipamento.modelo.ilike(termo),
                Equipamento.descricao.ilike(termo)
            )
        )
        
    # 3. Filtros Estritos (Passo 6.3)
    if categoria:
        query = query.filter(Equipamento.categoria == categoria)
        
    if preco_min is not None:
        query = query.filter(Equipamento.valor_diaria >= preco_min)
        
    if preco_max is not None:
        query = query.filter(Equipamento.valor_diaria <= preco_max)
        
    # 4. Ordenador Inteligente (Passo 6.4)
    if ordenar_por == 'menor_preco':
        query = query.order_by(asc(Equipamento.valor_diaria))
    elif ordenar_por == 'maior_preco':
        query = query.order_by(desc(Equipamento.valor_diaria))
    else:
        query = query.order_by(desc(Equipamento.id)) # Mais recentes primeiro
        
    # 5. Executa no Banco e Paginada
    return query.offset(skip).limit(limit).all()