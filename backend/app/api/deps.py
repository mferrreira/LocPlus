from fastapi import Depends, HTTPException, status
from app.core.security import get_current_user
from app.models.usuarios import Usuario

def get_current_tenant(current_user: Usuario = Depends(get_current_user)):
    """
    Middleware blindado: Verifica se o usuário atual pertence a um Tenant (Locadora).
    Se for apenas um Locatário ou se não tiver empresa atrelada, bloqueia o acesso a rotas do ERP.
    """
    if not current_user.empresa_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Acesso Negado: Esta conta não possui perfil de Locadora (Tenant)."
        )
    return current_user.empresa # Retorna objeto Empresa (ou pelo menos o ID)

from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.empresas import Empresa
from app.models.saas_core import Assinatura, Plano
from app.models.equipamentos import Equipamento

def verificar_limite_maquinas(
    current_tenant: Empresa = Depends(get_current_tenant),
    db: Session = Depends(get_db)
):
    """
    Middleware blindado SaaS: Verifica se o Tenant possui limite disponível no plano para cadastrar novas máquinas.
    """
    # 1. Busca a Assinatura vinculada à Empresa
    assinatura = db.query(Assinatura).filter(Assinatura.empresa_id == current_tenant.id).first()
    
    if not assinatura:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Operação negada: Nenhuma assinatura ativa foi encontrada para esta Locadora."
        )
        
    plano = assinatura.plano
    
    # 2. Conta quantas máquinas já estão vinculadas ao Tenant
    qtd_atual = db.query(Equipamento).filter(Equipamento.empresa_id == current_tenant.id).count()
    
    # 3. Valida contra o limite do Plano
    if qtd_atual >= plano.max_maquinas:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Limite excedido! O seu plano {plano.nome} permite o cadastro de até {plano.max_maquinas} máquinas. Atualmente você possui {qtd_atual} cadastradas."
        )
        
    return True
