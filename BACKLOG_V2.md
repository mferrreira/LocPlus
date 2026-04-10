# LocPlus - Visão de Futuro (V2) e Referências

Este documento é o nosso 'Cofre de Ideias' contínuo. Como a Fase 1 a 5 cobriu o MVP Funcional, usaremos este arquivo vivo para despejar links, referências de design e novos *Use Cases* à medida que o negócio evolui. Nenhuma destas tarefas é urgente ou para agora.

## 🎨 Referências de Mercado e Inspirações (Arquitetura e Design V2)
*Bases de alto nível para moldar a usabilidade (UI/UX) e modelagens de sistema do LocPlus.*

1. **Odoo Locação** ([odoo.com/documentation/19.0/developer.html](https://odoo.com/documentation/19.0/developer.html))
   - *Referência Principal:* Design, Usabilidade (UI/UX), Modelagem de Opções e documentação developer como base de alto nível.
2. **GestãoClick** ([gestaoclick.com](https://gestaoclick.com/))
3. **locApp** ([locapp.com.br](https://locapp.com.br/))
4. **Syspan Soluções Tecnológicas**

## 🚀 Novas Funcionalidades / Casos de Uso (Ongoing)
*Descreva as novas lógicas de negócio que vamos acoplar no sistema quando expandirmos o LocPlus.*

- [ ] **Pagamento Especial:** Acoplar Stripe ou Asaas para reter o Caução do cartão de crédito de forma transparente durante o aluguel.
- [ ] **Dashboard Analytics:** Gráficos interativos pro Locador ver o faturamento mensal.
- [ ] **Integração WhatsApp:** Disparar mensagem na API do zap quando a vistoria for concluída.

## 🛠️ Débitos Técnicos e Refatoração Pós-MVP
*O que fizemos em alta velocidade de DevOps que depois merecerá um toque arquitetural extra.*

- Refatorar a separação de Estado no React (avançar talvez para o Zustand ou Redux ToolKit se o estado global da Home e Auth pesar muito).
- Desmembrar os Super-Formulários (como o Cadastro.jsx) em *Wizards de 3 Passos* (Telas menores de Next/Prev).
