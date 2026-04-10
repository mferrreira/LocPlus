# Documento de Especificação de Produto e Arquitetura (PRD) - LOCPLUS

**Plataforma:** LocPlus - Sistema de Gestão e Marketplace para Locação de Máquinas e Ferramentas.
**Público-Alvo do Documento:** Engenharia de Software / Agente Antigravity.
**Referências de Mercado (UI/UX e Modelagem):** GestãoClick, locApp, Syspan Soluções Tecnológicas, Odoo Locação (Documentação base).

---

## 1. Visão Geral da Arquitetura e Stack Tecnológico
O LocPlus opera com uma arquitetura baseada em microsserviços conteinerizados, separando claramente as responsabilidades do motor de regras e da persistência de dados.

*   **Backend:** Python com FastAPI (alta performance e tipagem estrita via Pydantic).
*   **Banco de Dados:** PostgreSQL relacional (gerenciado via SQLAlchemy e Alembic para migrações).
*   **Storage (Arquivos/Imagens):** MinIO (S3-compatible) rodando em contêiner Docker para gestão de vistorias e fotos de máquinas.
*   **Segurança:** Autenticação via JWT (JSON Web Tokens) e hash de senhas via Bcrypt.
*   **Infraestrutura:** Orquestração local 100% via `docker-compose.yml`.

---

## 2. Escopo de Frontend e Funcionalidades por Módulo

A interface do LocPlus deve ser dinâmica e se adaptar com base no papel do usuário autenticado (Locador vs. Locatário)[cite: 6].

### Módulo 1: Dashboard e Página Inicial
A página inicial atua como o centro de comando do usuário.
*   **Interface Dinâmica:** A visualização inicial difere se a conta for de um locador (empresa/pessoa física) ou locatário[cite: 6].
*   **Atalhos e Navegação:** Atalhos diretos para Perfil, Máquinas, Ferramentas, Histórico, Financeiro, Gestão e Configuração[cite: 6]. A logo atua como botão "Home"[cite: 6].
*   **Motor de Sugestões:**
    *   Para locatários: Sugere máquinas baseadas em preferências e histórico de aluguéis[cite: 6].
    *   Para locadores: Exibe *leads* (clientes buscando por máquinas específicas que o locador possui)[cite: 6].
*   **Barra de Busca:** Centralizada, com autocomplete inteligente e aplicação de filtros dinâmicos[cite: 6].
*   **Central de Alertas e Notificações:**
    *   *Locatário:* Alertas de negociações aceitas, aluguéis em atraso ou disponibilidade de máquinas na lista de espera[cite: 6].
    *   *Locador:* Alertas de clientes interessados, propostas de negociação, problemas reportados em máquinas (chamados técnicos) e vistorias próximas do vencimento[cite: 6].
*   **Widgets Estratégicos (Cards):**
    *   *Locatário:* Quantidade de máquinas alugadas e atalho para ver o status de cada uma[cite: 6].
    *   *Locador:* Máquinas locadas vs. no pátio, além de um dashboard de rendimento financeiro mensal[cite: 6].
*   **Acesso Rápido Operacional:** Botões de emergência para abertura de chamados técnicos, vistorias pendentes e suporte da plataforma[cite: 6].

### Módulo 2: Autenticação e Onboarding (Login e Cadastro)
Fluxo focado em conversão e coleta progressiva de dados.
*   **Login:** Acesso via E-mail ou CPF/CNPJ e Senha, com opção "Lembrar de mim" e recuperação de senha via OTP (código) ou link enviado por e-mail/celular[cite: 4].
*   **Cadastro Passo 1:** O usuário define seu objetivo na plataforma ("Quero alugar" ou "Quero disponibilizar") e o tipo de entidade (PF ou PJ)[cite: 4].
*   **Fluxo Pessoa Física (PF):** Coleta de Nome completo, CPF, E-mail, Celular/WhatsApp e senha segura[cite: 4].
*   **Fluxo Pessoa Jurídica (PJ):** Coleta de CNPJ (com preenchimento automático de Razão Social/Fantasia), Inscrição Estadual, dados do responsável legal (Nome e CPF), E-mail corporativo, Celular/WhatsApp e senha segura[cite: 4].
*   **Validação (KYC):** Confirmação de contato via envio de código (E-mail ou WhatsApp), aceite obrigatório de Termos de Uso e Política de Privacidade[cite: 4]. Tela de sucesso informando sobre a futura necessidade de envio de documentação para análise antes da primeira locação[cite: 4].

### Módulo 3: Gestão de Perfil e Confiança
Centralização de dados fiscais e de segurança.
*   **Dados Cadastrais:** Separação clara entre campos PF (Nome, CPF, RG, Nascimento) e PJ (Razão Social, Nome Fantasia, CNPJ, IE)[cite: 5].
*   **Gestão de Endereços:** Cadastro de endereço Sede/Matriz e múltiplos endereços (Canteiros de Obras) para cálculo otimizado de frete[cite: 5].
*   **Segurança e LGPD:** Upload de documentos (Contrato Social, CNH/RG, Comprovante de Endereço) com exibição de "Status de Verificação"[cite: 5]. Opções para 2FA, gestão de sessões ativas e exclusão/download de dados (LGPD)[cite: 5]. O histórico também pode ter sua visibilidade configurada[cite: 5].
*   **Financeiro e Vitrine:** Dados bancários para repasses (Locador) e métodos de pagamento/faturamento (Locatário)[cite: 5]. Criação de um Perfil Público (Vitrine) personalizável com logo, descrição, horário e avaliação por estrelas[cite: 5].
*   **Locação por Representação (Feature B2B Avançada):**
    *   Permite ao locatário alugar em nome de terceiros usando sua própria conta[cite: 5].
    *   Exige upload de comprovante de vínculo e declaração de autorização assinada pelo responsável final[cite: 5].
    *   Faturamento direcionado: Emissão de Nota Fiscal e entrega para os dados do cliente final, mantendo o representante logado como administrador da locação[cite: 5].

### Módulo 4: Cadastro de Equipamentos (Wizard)
Um fluxo educativo em 6 passos para garantir dados ricos no catálogo.
*   **Passo 1 (Identificação):** Categoria, Subcategoria, Título do anúncio, Marca, Modelo e Ano[cite: 3].
*   **Passo 2 (Especificações):** Chassi/Série (com ajuda visual) e campos técnicos dinâmicos baseados na categoria (Ex: KVA para geradores)[cite: 3]. Inclusão de tutoriais rápidos embutidos[cite: 3].
*   **Passo 3 (Vistoria e Transparência):** Upload obrigatório de fotos (Geral, painel, motor), campo para relato de avarias estéticas pré-existentes e data da última manutenção preventiva[cite: 3].
*   **Passo 4 (Precificação):** Valores modulares (Diária, Semana, Quinzena, Mês), tempo mínimo e exigência de caução protetiva[cite: 3].
*   **Passo 5 (Logística):** Endereço do pátio, disponibilidade de entrega (raio em km e taxa) ou apenas retirada[cite: 3].
*   **Passo 6 (Publicação):** Calendário de bloqueio de datas (manutenção/locação externa), tela de resumo geral e botão de publicação[cite: 3].

### Módulo 5: Motor de Regras e Vistoria Digital
O coração operacional do sistema, blindando as duas partes.
*   **Check-out (Entrega pelo Locador):** Captura fotográfica em tempo real (bloqueando envio da galeria), registro de horímetro/odômetro, nível de combustível/carga elétrica e checklist de avarias por botões (Pneus, Vidros, etc.)[cite: 2].
*   **Check-in (Aceite do Locatário):** Tela de transparência exibindo os dados da entrega[cite: 2]. Prazo legal de 12 horas úteis para contestação fotográfica de divergências[cite: 2]. Aceite final por assinatura digital ou botão[cite: 2].
*   **Devolução e Cobranças Extras:** Nova vistoria obrigatória no recolhimento. Cálculo automático via horímetro para cobrança de horas excedentes[cite: 2]. Validação de limpeza e combustível, habilitando taxa extra se não retornar no padrão[cite: 2].
*   **Proteção de Máquina Parada:** Botão de "Assistência" que congela as diárias automaticamente até a resolução[cite: 2]. Locador tem prazo (24h/48h) para conserto ou substituição, sob pena de cancelamento e estorno[cite: 2]. Regra de "Desgaste Natural" isenta o locatário de manutenções corretivas internas[cite: 2].
*   **Resolução de Conflitos:** Abertura de sinistro pelo locador com bloqueio da caução[cite: 2]. Exigência de laudo técnico de oficina isenta para cobrança de danos não-estéticos[cite: 2]. Ambiente de mediação para aprovação de orçamento entre as partes[cite: 2].

### Módulo 6: Busca e Filtros Inteligentes
Foco em conversão e usabilidade guiada.
*   **Busca Guiada (Assistente):** Botão "Não sabe o que usar?" que aciona um questionário dinâmico sobre a necessidade[cite: 1]. Ao final, o assistente aplica os filtros automaticamente na barra de busca principal em vez de criar uma página paralela[cite: 1].
*   **Catálogo Estático e Lista de Espera:** Filtros sempre visíveis mesmo sem estoque (botão "Avise-me quando chegar")[cite: 1]. Máquinas alugadas aparecem nos resultados em cinza com a tag "Alugada no momento", habilitando o alerta de disponibilidade futura[cite: 1].
*   **Filtros B2B:** Geolocalização/Raio de distância, especificações dinâmicas por categoria (Ex: capacidade), opções comerciais (preço, caução, entrega)[cite: 1].
*   **Visualização e Ordenação:** Alternância entre "Lista de Cards" ou "Mapa de Máquinas"[cite: 1]. Ordenação por preço, distância ou avaliação do locador[cite: 1].

---

## Instruções para o Agente Antigravity

1.  **Revisão Arquitetural:** Avalie o escopo acima e sugira melhorias na modelagem do banco de dados (esquemas do PostgreSQL) para suportar a complexidade do módulo de "Vistoria Digital" e "Locação por Representação".
2.  **UX/UI Flow:** Ao gerar as telas no frontend, garanta que os formulários de cadastro de máquinas (Módulo 4) sejam estritamente divididos em etapas (Wizard) para não sobrecarregar a carga cognitiva do usuário.
3.  **Sugestões:** Sinta-se livre para propor *design patterns* melhores a médio e longo prazo, desde que não fujam das referências centrais (GestãoClick, Odoo).