# LocPlus - Plataforma de Aluguel de Máquinas e Ferramentas

## 0. Guia de Engenharia e Arquitetura (Technical Guidelines)

Para o funcionamento contínuo e autônomo de agentes de IA neste projeto, siga estritamente as restrições arquiteturais detalhadas abaixo.

### 0.1 Stack Tecnológica (Tech Stack)
* **Backend:** Python + **FastAPI**.
* **Banco de Dados Relacional:** **PostgreSQL** (acessado via `psycopg`).
* **ORM & Migrations:** **SQLAlchemy 2.0** para modelagem relacional e **Alembic** para controle de versão do banco.
* **Autenticação:** **JWT** (via `PyJWT`) com hash de senhas via `bcrypt`.
* **Validação de Dados:** **Pydantic** v2.
* **Frontend:** A definir. Sugere-se **React/Next.js** com **TailwindCSS** para viabilizar as interfaces descritas.

### 0.2 Padrões de Código e Estrutura de Pastas (Backend)
O diretório `backend/` já obedece um padrão estrutural sólido que **não deve ser quebrado**:
* `/app/api/`: Controladores e rotas (Endpoints).
* `/app/core/`: Configurações centrais e segurança (JWT).
* `/app/models/`: Entidades de banco de dados (SQLAlchemy Models).
* `/app/schemas/`: Modelos para validação HTTP (Pydantic Schemas).
* `/alembic/`: Sempre que um novo modelo (`models/`) for criado, é obrigatório gerar uma migration no Alembic.

### 0.3 Fases e Status Atual (Backend Roadmap)
*(Status atualizado via auditoria do código fonte. O Agente deve focar exclusivamente nos checkboxes vazios `[ ]`)*

* **[EM ANDAMENTO] Fase 1: Fundação & Autenticação (Backend Setup)**
  * [x] Criação da estrutura base DDD (models, schemas, api, core).
  * [x] Configuração central do FastAPI e arquivos base (`main.py`).
  * [ ] Revisar rotas de Auth (JWT/Login) e verificar se `usuarios.py` possui diferenciação correta de PF/PJ exigida no PRD.

* **[EM ANDAMENTO] Fase 2: Domínio de Máquinas/Ferramentas (CRUD Core)**
  * [x] CRUD Básico de `Equipamento` configurado.
  * [ ] Adicionar campos técnicos faltantes no Model e Schema (Marca, Modelo, Ano, Preços Modulares - Passo 4.1 e 4.4).
  * [ ] Implementar rota de upload de fotos reais no endpoint de equipamentos. (Passo 4.3).
  * [ ] Adicionar calendário dinâmico / bloqueio de datas.

* **[CONCLUÍDA] Fase 3: Catálogo, Buscas e Vitrine**
  * [x] Aprimoramento do SQLAlchemy Engine (`GET /equipamentos` recebe Query Parameters inteligentes como Passo 6).

* **[CONCLUÍDA] Fase 4: O Coração do Negócio (Contratos e Vistorias)**
  * [x] Entidade `Locacao` existe e abate o estoque corretamente na criação.
  * [x] Entidade `Vistorias` alterada para salvar métricas precisas (Horímetro, Checklists) e fotos via MinIO.
  * [x] Máquina de Estados da Vistoria Digital criada (`POST /locacoes/{id}/aceite`).
  * [x] API de 'Máquina Parada' e pausa de contrato criada (`POST /locacoes/{id}/maquina-parada`).

* **[CONCLUÍDA] Fase 5: Integração Frontend**
  * [x] Fases 1 a 4 100% testadas.
  * [x] React Puro, Vite e Tailwind UI Clean montados.
  * [x] Fluxos Híbridos: `Buscas Híbridas`, `Auth` e `Painel Field para Câmera Nativa` estruturados.

---

## 1. Regras de Negócio e Funcionalidades (PRD)
*(As diretrizes abaixo ditam o produto final e são a interface para o usuário)*

1. Pagina Inicial
  1.1 Montar interface inicial do projeto
    1.1.1 Ter em mente que a interface inicial do projeto deve ser diferente caso a conta seja de uma empresa/pessoa fisica locador e de uma e uma empresa/pessoa fisica locatario
    1.1.2 Adicionar atalhos simples para outras telas, como Perfil, Maquinas, Ferramentas, Historico, Financeiro, Gestão e Configuração.
    1.1.3 Adicionar sugestões na tela do locatario de maquinas ou ferramentas, baseado na preferencia do usuario e seu historico.
    1.1.4 Adicionar sugestões na tela do locador de clientes que necessitam de alguma maquina ou ferramenta e estão buscando por elas

2. Página de Perfil (Visão Geral e Dados do Usuário)
  2.1 Montar a interface de dados cadastrais (Diferenciada por PF e PJ)
    2.1.1 Para Pessoa Física (Locatário): Nome completo, CPF, RG e Data de Nascimento.
    2.1.2 Para Pessoa Jurídica (Locador ou Locatário): Razão Social, Nome Fantasia, CNPJ e Inscrição Estadual.
    2.1.3 Informações de Contato unificadas: E-mail principal do responsável, telefone fixo comercial e celular/WhatsApp.
  2.2 Endereços e Geolocalização

3. Página de Login e Cadastro (Autenticação)
  3.1 Tela de Login (Acesso ao Sistema)
    3.1.1 Campos de entrada padrão: E-mail (ou CPF/CNPJ) e Senha.
    3.1.2 Opção "Lembrar de mim" para manter a sessão do usuário ativa.
    3.1.3 Link para "Esqueci minha senha", com fluxo de recuperação enviando um código (OTP) ou link para o e-mail ou celular cadastrado.
  3.2 Tela de Cadastro Inicial (Onboarding)

4. Cadastro de Máquinas e Ferramentas (Formato Wizard / Passo a Passo)
  4.1 Passo 1: O que você está alugando? (Identificação Básica)
    4.1.1 Escolha da Categoria Principal e Subcategoria (ex: Linha Amarela > Retroescavadeira).
    4.1.2 Título do anúncio (como o cliente verá).
    4.1.3 Marca, Modelo e Ano de Fabricação.
  4.2 Passo 2: Especificações e Numerações (Com UX Educativo)
    4.2.1 Número de Série ou Chassi (com ícone/botão de ajuda visível: "Onde encontro essa numeração no meu equipamento?").
    4.2.2 Campos técnicos dinâmicos gerados a partir da categoria escolhida no Passo 1 (ex: se for gerador, pede KVA; se for guindaste, pede capacidade de carga).
    4.2.3 Tutorial embutido: Textos curtos ou vídeos rápidos fixados ao lado de campos técnicos mais complexos, explicando exatamente como preencher.
  4.3 Passo 3: Transparência e Estado de Conservação (Vistoria)
    4.3.1 Upload de fotos obrigatórias (Visão geral, painel de controle, motor/bateria).
    4.3.2 Campo de "Observações de Avarias": Espaço claro para o locador relatar arranhões, barulhos ou detalhes estéticos pré-existentes.
    4.3.3 Data da última manutenção preventiva ou vistoria realizada.
  4.4 Passo 4: Precificação e Regras do Aluguel
    4.4.1 Tabela de valores modulares: Preço por Diária, Semana, Quinzena e Mês.
    4.4.2 Definição de tempo mínimo de locação.
    4.4.3 Exigência de caução protetiva (Sim/Não) e valor estipulado.
  4.5 Passo 5: Logística e Entrega
    4.5.1 Endereço atual de onde a máquina se encontra (Pátio de origem).
    4.5.2 Definição de frete: O locador entrega? Se sim, qual o raio de quilometragem (ex: atende até 50km) e qual a taxa? Ou a retirada é exclusiva pelo cliente?
  4.6 Passo 6: Revisão e Disponibilidade
    4.6.1 Calendário para bloqueio de datas (caso a máquina já tenha manutenções agendadas ou locações por fora).
    4.6.2 Tela de resumo mostrando tudo o que foi preenchido nos passos anteriores para conferência final.
    4.6.3 Botão final de "Salvar e Publicar Anúncio"

5. Regras e Fluxo de Vistoria Digital
  5.1 Vistoria de Entrega (Check-out feito pelo Locador)
    5.1.1 Captura em tempo real: O sistema deve abrir a câmera do aplicativo/site, bloqueando o upload de fotos antigas da galeria para garantir que a foto é do exato momento da entrega.
    5.1.2 Registro do Horímetro/Odômetro atual (essencial para controle da franquia de horas e manutenções).
    5.1.3 Marcação do nível de combustível ou nível de carga (para baterias elétricas).
    5.1.4 Checklist visual rápido em botões: Pneus/Esteiras, Vidros, Painel, Lataria e Mangueiras Hidráulicas (status: "Ok" ou "Avariado").
  5.2 Aceite de Recebimento (Check-in feito pelo Locatário)
    5.2.1 Tela de transparência: O cliente visualiza as fotos, o horímetro e o checklist enviados pelo locador antes de começar a usar.
    5.2.2 Prazo limite de contestação: O cliente tem até 12 horas úteis após a entrega física para tirar uma foto apontando divergências (ex: a máquina chegou suja ou com menos combustível do que o relatado).
    5.2.3 Assinatura digital ou aceite por botão confirmando que a máquina foi recebida nas exatas condições descritas no sistema.
  5.3 Vistoria de Devolução (Retorno ao Locador)
    5.3.1 Novo registro fotográfico obrigatório no momento do recolhimento da máquina.
    5.3.2 Leitura final do Horímetro/Odômetro (para o sistema calcular automaticamente se o cliente excedeu o limite de horas do contrato e gerar cobrança extra).
    5.3.3 Validação de limpeza e combustível (com opção do locador acionar a cobrança de taxa de lavagem ou reabastecimento caso não retorne como foi entregue).
  5.4 Proteção ao Locatário (Falhas e Desgaste Durante o Uso)
    5.4.1 Botão de "Assistência / Máquina Parada": Um atalho rápido no painel do cliente para notificar imediatamente que o equipamento apresentou falha técnica durante a operação.
    5.4.2 Congelamento de Diárias: Ao acionar o botão de máquina parada, o sistema pausa automaticamente a contagem do tempo de locação até que a máquina seja consertada ou substituída, garantindo que o cliente não pague por um equipamento inoperante.
    5.4.3 Regra do Desgaste Natural: Estabelecer nos Termos de Uso que falhas internas (motor, transmissão, fadiga de material) são de responsabilidade do Locador, isentando o Locatário de custos de manutenção corretiva, exceto em casos de mau uso comprovado.
    5.4.4 Obrigação de Substituição ou Estorno: O Locador recebe um prazo (ex: 24h ou 48h) para consertar a máquina no local ou enviar uma substituta. Caso não cumpra, o Locatário ganha o direito de cancelar o contrato sem multas e receber o estorno dos dias não utilizados.
  5.5 Tratativa de Avarias e Conflitos (Resolução de Disputas)
    5.5.1 Abertura de Sinistro: O locador sinaliza o problema (ex: peça quebrada na devolução por mau uso) anexando fotos do dano.
    5.5.2 Retenção de Caução: O valor da caução fica temporariamente bloqueado no sistema.
    5.5.3 Exigência de Laudo Técnico: Para que o Locador possa cobrar do Locatário uma quebra que ocorreu durante o uso (e não um dano estético visível na devolução), a plataforma exigirá o upload de um laudo de uma oficina isenta comprovando falha operacional/mau uso, protegendo o cliente de cobranças arbitrárias.
    5.5.4 Ambiente de Acordo: Tela dedicada para o locador enviar o orçamento e o cliente aprovar ou contestar o pagamento, com a plataforma atuando como mediadora final caso não haja acordo.

6. Fluxo de Busca e Filtros
  6.1 Busca Tradicional (Para quem já sabe o que quer)
    6.1.1 Barra de pesquisa principal com autocompletar (sugerindo categorias, marcas e nomes de máquinas enquanto o usuário digita).
    6.1.2 Histórico de buscas recentes salvo na interface.
  6.2 Assistente Inteligente de Busca (Busca Guiada e Ativador de Filtros)
    6.2.1 Acesso em destaque: Um botão chamativo na barra de busca (Ex: "Não sabe qual máquina usar? Nós te ajudamos").
    6.2.2 Fluxo de perguntas dinâmicas para mapear a necessidade (tipo de serviço, ambiente, exigência de capacidade).
    6.2.3 Ação Automação de Filtro: Ao final das respostas, o assistente não cria uma página nova, ele simplesmente aplica os filtros correspondentes de forma automática na barra de busca principal. O sistema então exibe todas as máquinas/ferramentas que possuem aquelas tags ativas.
  6.3 Filtros Avançados e Fixos (Refinamento B2B)
    6.3.1 Catálogo Estático de Filtros: Todas as categorias e tipos de máquinas/ferramentas devem estar sempre listadas nos filtros laterais, mesmo que não haja nenhuma máquina daquele tipo cadastrada no momento (podendo exibir um aviso de "0 resultados" ao lado ou uma opção de "Avise-me quando chegar").
    6.3.2 Geolocalização e Raio de Distância: Para calcular viabilidade de frete.
    6.3.3 Disponibilidade e Lista de Espera: Equipamentos já locados no período desejado não serão ocultados dos resultados. Eles permanecerão visíveis, porém com a interface inativa (imagem em tons de cinza) e um selo/tag visual de "Alugada no momento".
    6.3.4 Botão "Avise-me quando disponível": Inserção de uma ferramenta nas máquinas alugadas para que o cliente possa marcá-las. O sistema disparará uma notificação automática (conforme o painel de alertas do item 1.1.7) assim que o contrato atual daquela máquina for encerrado e ela retornar ao catálogo.
    6.3.5 Filtros Técnicos Dinâmicos: Mostrar especificações baseadas na categoria selecionada (Ex: KVA para geradores).
    6.3.6 Filtros Comerciais: Faixa de preço, exigência de caução, opção de entrega.
  6.4 Visualização e Ordenação de Resultados
    6.4.1 Alternância de visualização: "Lista de Cards" ou "Mapa".
    6.4.2 Ordenação inteligente: Menor preço, Mais próximos, Maior nota de avaliação da empresa.
