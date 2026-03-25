from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Form
from sqlalchemy.orm import Session
from uuid import uuid4
from app.core.database import get_db
from app.core.storage import upload_file_to_minio
from app.models.vistorias import Vistoria, TipoVistoria
from app.models.locacoes import Locacao
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
    db: Session = Depends(get_db)
):
    locacao = db.query(Locacao).filter(Locacao.id == locacao_id).first()
    if not locacao:
        raise HTTPException(status_code=404, detail="Contrato não encontrado.")

    foto_url = None
    if foto:
        nome_arquivo = f"vistoria_{locacao_id}_{tipo.value}_{uuid4()}.{foto.filename.split('.')[-1]}"
        foto_url = upload_file_to_minio(foto, nome_arquivo)

    nova_vistoria = Vistoria(
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