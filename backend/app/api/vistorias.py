from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Form
from sqlalchemy.orm import Session
import shutil
import os
from uuid import uuid4 # Gerador de códigos únicos impressionantes

from app.core.database import get_db
from app.models.vistorias import Vistoria, TipoVistoria
from app.models.locacoes import Locacao
from app.schemas.vistorias import VistoriaResponse

router = APIRouter(prefix="/vistorias", tags=["Vistorias e Uploads de Fotos"])

# Onde as fotos vão morar no seu computador (O Python criará essa pasta automaticamente)
UPLOAD_DIR = "uploads/vistorias"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# Atenção: Usamos Form() e File() em vez do Schema de Create padrão
@router.post("/", response_model=VistoriaResponse, status_code=status.HTTP_201_CREATED)
def registrar_vistoria(
    locacao_id: int = Form(...),
    tipo: TipoVistoria = Form(...),
    observacoes: str = Form(None),
    foto: UploadFile = File(None),
    db: Session = Depends(get_db)
):
    # 1. Trava de Segurança: Este contrato de aluguel existe?
    locacao = db.query(Locacao).filter(Locacao.id == locacao_id).first()
    if not locacao:
        raise HTTPException(status_code=404, detail="Contrato de locação não encontrado.")

    foto_url = None

    # 2. Processamento Físico da Imagem
    if foto:
        # Pega a extensão original (.jpg, .png)
        extensao = foto.filename.split(".")[-1]
        # Cria um nome impossível de repetir (ex: 550e8400-e29b-41d4-a716-446655440000.jpg)
        nome_arquivo = f"{uuid4()}.{extensao}"
        caminho_completo = os.path.join(UPLOAD_DIR, nome_arquivo)
        
        # Salva a imagem no SSD
        with open(caminho_completo, "wb") as buffer:
            shutil.copyfileobj(foto.file, buffer)
        
        # Este é o texto que vai para o PostgreSQL
        foto_url = caminho_completo

    # 3. Gravação no Banco de Dados
    nova_vistoria = Vistoria(
        locacao_id=locacao_id,
        tipo=tipo,
        observacoes=observacoes,
        fotos_url=foto_url
    )
    
    db.add(nova_vistoria)
    db.commit()
    db.refresh(nova_vistoria)

    return nova_vistoria