from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Form
from sqlalchemy.orm import Session
from uuid import uuid4
from app.core.database import get_db
from app.core.storage import upload_file_to_minio
from app.api.deps import get_current_tenant
from app.models.empresas import Empresa
from typing import List
from app.models.vistorias import Vistoria, TipoVistoria
from app.models.locacoes import Locacao, StatusLocacao
from app.models.equipamentos import Equipamento
from app.schemas.vistorias import VistoriaResponse

router = APIRouter(prefix="/vistorias", tags=["Vistorias e Inspeções Digitais"])

# Atenção: Usamos Form() e File() em vez do Schema de Create padrão
@router.post("/", response_model=VistoriaResponse, status_code=status.HTTP_201_CREATED)
def registrar_vistoria(
    locacao_id: int = Form(...),
    tipo: TipoVistoria = Form(...),
    horimetro_odometro: float = Form(0.0),
    nivel_combustivel: str = Form("Cheio"),
    check_pneus: bool = Form(True),
    check_vidros: bool = Form(True),
    check_lataria: bool = Form(True),
    check_painel: bool = Form(True),
    check_hidraulica: bool = Form(True),
    observacoes: str = Form(None),
    foto: UploadFile = File(None),
    db: Session = Depends(get_db),
    current_tenant: Empresa = Depends(get_current_tenant)
):
    locacao = db.query(Locacao).filter(
        Locacao.id == locacao_id,
        Locacao.empresa_id == current_tenant.id
    ).first()
    
    if not locacao:
        raise HTTPException(status_code=404, detail="Contrato não encontrado nesta Locadora.")

    foto_url = None
    if foto:
        nome_arquivo = f"{current_tenant.id}/vistorias/vistoria_{locacao_id}_{tipo.value}_{uuid4()}.{foto.filename.split('.')[-1]}"
        foto_url = upload_file_to_minio(foto, nome_arquivo)

    nova_vistoria = Vistoria(
        empresa_id=current_tenant.id,
        locacao_id=locacao_id,
        tipo=tipo,
        horimetro_odometro=horimetro_odometro,
        nivel_combustivel=nivel_combustivel,
        check_pneus=check_pneus,
        check_vidros=check_vidros,
        check_lataria=check_lataria,
        check_painel=check_painel,
        check_hidraulica=check_hidraulica,
        observacoes=observacoes,
        fotos_url=foto_url
    )
    
    db.add(nova_vistoria)
    db.commit()
    db.refresh(nova_vistoria)

    return nova_vistoria

# ==========================================
# FLUXO DE DEVOLUÇÃO E ENCERRAMENTO
# ==========================================
@router.post("/{locacao_id}/devolucao", response_model=VistoriaResponse, status_code=status.HTTP_201_CREATED)
def registrar_devolucao(
    locacao_id: int,
    horimetro_final: float = Form(...),
    checklist_status: str = Form(...),
    fotos: List[UploadFile] = File(...),
    db: Session = Depends(get_db),
    current_tenant: Empresa = Depends(get_current_tenant)
):
    # 1. Trava de Tenant: Este contrato de devolução é DESTA locadora?
    locacao = db.query(Locacao).filter(
        Locacao.id == locacao_id,
        Locacao.empresa_id == current_tenant.id
    ).first()
    
    if not locacao:
        raise HTTPException(status_code=404, detail="Contrato não encontrado nesta Locadora.")
    
    if locacao.status == StatusLocacao.FINALIZADO:
        raise HTTPException(status_code=400, detail="Este contrato já está finalizado e a vistoria foi feita.")

    # 2. Upload Múltiplo pro S3 Cloud Storage
    fotos_salvas = []
    for foto in fotos:
        if foto.filename:
            nome_arq = f"{current_tenant.id}/vistorias/{locacao_id}/devolucao_{uuid4()}.{foto.filename.split('.')[-1]}"
            s3_url = upload_file_to_minio(foto, nome_arq)
            fotos_salvas.append(s3_url)
            
    todas_as_fotos_str = ",".join(fotos_salvas) if fotos_salvas else None

    # 3. Registrar a Vistoria Transacional
    nova_vistoria = Vistoria(
        empresa_id=current_tenant.id,
        locacao_id=locacao_id,
        tipo=TipoVistoria.DEVOLUCAO,
        horimetro_odometro=horimetro_final,
        observacoes=checklist_status,
        fotos_url=todas_as_fotos_str
    )
    db.add(nova_vistoria)

    # 4. Transação Fina: Mudar Status e Liberar Estoque
    locacao.status = StatusLocacao.FINALIZADO
    
    equipamento = db.query(Equipamento).filter(Equipamento.id == locacao.equipamento_id).first()
    if equipamento:
        equipamento.quantidade_disponivel += 1
        
    db.commit()
    db.refresh(nova_vistoria)
    
    return nova_vistoria