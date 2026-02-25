# Feature Requirements: overspec-dev

| Field    | Value                      |
|----------|----------------------------|
| Project  | overspec-dev               |
| Date     | 2026-02-25                 |
| Version  | 3.0                        |
| Agent    | penny                      |
| Phase    | Discovery (New Features)   |
| Based on | Impact Analysis by raj     |

---

## Executive Summary

Adicionar ao OverSpec uma **Design Specialist** — uma agente completa que combina **Atomic Design** (hierarquia de componentes), **art direction** (estética intencional, anti-genérica), **design tokens**, **especificação de UI/UX**, **acessibilidade (WCAG)**, **motion design** e **implementação frontend production-grade**. A agente opera numa fase opcional de design (entre architecture e implementation) e entrega artifacts que guiam Howard na implementação, incluindo código frontend funcional quando aplicável.

**Mudança de escopo vs. análise do Raj:** O escopo expandiu. Além de especificação de design (documentação), a agente também produz **código frontend production-grade** — componentes, páginas, pequenas apps — com art direction distintiva. Isso a diferencia de uma agente de "spec only".

---

## Features

### F1 — Agent Definition: Design Specialist

**Description:** Criar a agente design-specialist com persona, princípios, activation sequence, behaviors, outputs e consumes. A agente combina dois domínios: (1) **Atomic Design** para estrutura de componentes e (2) **Frontend Design** para implementação visual com art direction.

**User/Persona:** Desenvolvedores e equipes que usam OverSpec para construir software com interfaces de usuário.

**Impact Summary (from Raj):** 1 arquivo novo (agent YAML ~300-400 linhas), 3 arquivos modificados (_schema.json, overspec.yaml, spec.yaml). Risco baixo.

#### Functional Requirements

- **FR-1.1:** A agente deve ter `model_role: "designer"` — novo role a ser adicionado ao schema e model_profiles
- **FR-1.2:** A agente deve seguir a metodologia Atomic Design (atoms → molecules → organisms → templates → pages)
- **FR-1.3:** A agente deve ter a skill completa de Frontend Design integrada na persona, incluindo:
  - Estabelecer brief (propósito, usuário-alvo, ação primária, densidade de conteúdo)
  - Definir art direction explícita (não "safe default") com nome, rationale e 3 motifs assinatura
  - Criar design tokens primeiro (CSS variables: cores, tipografia, spacing, efeitos)
  - Implementar layout e componentes (composition first, estados: hover, active, focus-visible, disabled, loading, empty)
  - Motion pass (entrada orquestrada, prefers-reduced-motion)
  - Accessibility & quality gates (semântica HTML, keyboard nav, contraste, responsivo, performance)
- **FR-1.4:** A agente deve ter guardrails anti-genéricos — não usar padrões "AI UI" previsíveis, card grids genéricos, paletas tímidas ou gradientes purple-on-white
- **FR-1.5:** A agente deve propor 2-3 opções de art direction quando requisitos são fracos, recomendar uma, e prosseguir
- **FR-1.6:** A agente deve produzir código production-grade e funcional — não pseudo-código
- **FR-1.7:** A agente deve incluir pelo menos um "memorability hook" em cada design — um detalhe que alguém consiga descrever de memória
- **FR-1.8:** A agente deve respeitar convenções do codebase existente quando integra (CSS approach, naming, component structure)
- **FR-1.9:** A agente deve ter phases: `[design]` e poder participar de party-mode para discussões de design

#### Non-Functional Requirements

- **NFR-1.1:** A definição do agente deve seguir o padrão dos agentes existentes (formato YAML, seções obrigatórias)
- **NFR-1.2:** A persona deve ter personalidade distinta inspirada em personagem do Big Bang Theory (manter coerência com o roster)
- **NFR-1.3:** Activation sequence deve incluir context monitoring (como os outros 5 specialist agents)

#### Acceptance Criteria

- **AC-1.1:** Given o arquivo `design-specialist.agent.yaml` existe, When validado contra `_schema.json`, Then passa sem erros
- **AC-1.2:** Given a agente é ativada, When recebe um pedido de design, Then segue o workflow de 6 passos (brief → art direction → tokens → layout → motion → a11y)
- **AC-1.3:** Given requisitos fracos do usuário, When a agente inicia, Then propõe 2-3 opções de art direction antes de prosseguir
- **AC-1.4:** Given a agente produz código, When o código é entregue, Then inclui design tokens centralizados, estados de interação, responsividade e suporte a prefers-reduced-motion

#### Business Rules

- A fase de design é **opcional** — projetos que não têm UI podem pular
- A agente **não substitui** Leonard (architect) — Leonard decide estrutura do sistema, a design specialist decide estrutura visual
- Quando integra em codebase existente, a agente **preserva convenções** e isola tokens/theme ao escopo da feature
- A agente **nunca produz design genérico** — cada output deve ter art direction intencional

---

### F2 — Design Workflows: 3 Tracks

**Description:** Criar workflows de design para os 3 tracks (greenfield, brownfield, new-features). Cada workflow tem 4 arquivos padrão e guia a agente pelo processo de design.

**User/Persona:** A própria agente e Sheldon (para roteamento).

**Impact Summary (from Raj):** 12 arquivos novos (4 por track), 3 arquivos modificados (overspec.yaml, spec.yaml, sheldon). Risco médio.

#### Functional Requirements

- **FR-2.1:** Workflow **greenfield** (`3.5-design/`) deve cobrir design system completo:
  - Atomic Design hierarchy (atoms → pages)
  - Design tokens (CSS variables)
  - Art direction (nome, rationale, motifs)
  - UI specification (layouts, componentes, estados, responsivo)
  - Motion specification
  - Accessibility requirements
  - Código frontend de referência (componentes-chave)
- **FR-2.2:** Workflow **brownfield** (`bf-2.5-design/`) deve cobrir:
  - Audit do design existente (o que existe, o que está inconsistente)
  - Plano de melhoria do design system
  - Design tokens para padronizar o que já existe
  - Recomendações de art direction para unificar
- **FR-2.3:** Workflow **new-features** (`nf-3.5-design/`) deve cobrir:
  - Design da feature integrando ao design system existente (ou criando um se não houver)
  - UI specification da feature específica
  - Componentes novos necessários (com código)
  - Design tokens novos ou extensões dos existentes
- **FR-2.4:** Cada workflow deve ter steps claros que seguem o fluxo: brief → art direction → tokens → layout/components → motion → a11y
- **FR-2.5:** A fase de design deve ser `required: false` nos 3 tracks (opcional)
- **FR-2.6:** A fase de design deve ficar na posição `order: 3.5` (greenfield/new-features) e `order: 2.5` (brownfield) — entre architecture e implementation
- **FR-2.7:** Input dos workflows deve consumir artifacts de Leonard (architecture) e Penny (requirements/stories)
- **FR-2.8:** Output dos workflows deve ir para `artifacts/design/` e ser consumido por Howard (implementation) e Amy (review)

#### Non-Functional Requirements

- **NFR-2.1:** Workflows devem seguir o padrão de 4 arquivos (yaml + instructions + template + checklist)
- **NFR-2.2:** Instructions devem incluir language protocol e communication tone
- **NFR-2.3:** Checklists devem ter items required com critérios mensuráveis

#### Acceptance Criteria

- **AC-2.1:** Given os 3 diretórios de workflow existem, When cada um é inspecionado, Then contém 4 arquivos (workflow.yaml, instructions.md, template.md, checklist.md)
- **AC-2.2:** Given o workflow greenfield é executado, When a agente conclui, Then produz artifacts em `artifacts/design/` com design system, tokens e UI spec
- **AC-2.3:** Given a fase de design é skipped (usuário opta por pular), When o state machine avança, Then pula diretamente para implementation sem erros
- **AC-2.4:** Given o workflow tem handoff_to, When a agente conclui, Then o handoff aponta para howard

#### Business Rules

- Brownfield design audit deve respeitar o princípio de "evolução, não revolução" — melhorar incrementalmente, não reescrever
- New-features design deve integrar com design system existente quando possível
- Se não existe design system prévio, o workflow de new-features deve criar um mínimo viável

---

### F3 — Integration: Teams, Sheldon, Artifacts

**Description:** Integrar a design specialist no ecossistema: atualizar teams, phase maps do Sheldon, schema, model profiles e diretório de artifacts.

**User/Persona:** Sheldon (roteamento), Amy (review), Howard (consumir artifacts de design).

**Impact Summary (from Raj):** 4+ arquivos modificados (teams, sheldon, schema, overspec.yaml). Risco baixo.

#### Functional Requirements

- **FR-3.1:** Adicionar `"designer"` ao enum `model_role` em `_schema.json`
- **FR-3.2:** Adicionar `designer` aos 3 model_profiles em `overspec.yaml` (quality: opus, balanced: opus, budget: sonnet)
- **FR-3.3:** Adicionar fase `design` com `required: false` e `order` correto nos 3 tracks de `overspec.yaml`
- **FR-3.4:** Atualizar `team-fullstack.yaml`, `team-newfeatures.yaml` e `team-brownfield.yaml` para incluir design-specialist
- **FR-3.5:** Registrar agente e workflows em `spec.yaml`
- **FR-3.6:** Atualizar phase maps do Sheldon para mostrar a fase de design nos 3 tracks
- **FR-3.7:** Atualizar `new_project_detection` do Sheldon para mencionar a design specialist quando relevante
- **FR-3.8:** Diretório `artifacts/design/` deve existir com `.gitkeep`

#### Non-Functional Requirements

- **NFR-3.1:** `team-quick.yaml` NÃO deve incluir design-specialist (quick fix não precisa de design)
- **NFR-3.2:** Todas as mudanças devem ser backward-compatible — projetos existentes sem fase de design continuam funcionando

#### Acceptance Criteria

- **AC-3.1:** Given `_schema.json` é lido, When o campo model_role é inspecionado, Then inclui "designer"
- **AC-3.2:** Given overspec.yaml é lido, When as fases são listadas, Then cada track tem fase `design` com `required: false`
- **AC-3.3:** Given os 3 team presets são lidos, When os agentes são listados, Then incluem design-specialist
- **AC-3.4:** Given Sheldon apresenta o phase map, When o track é greenfield, Then mostra: Discovery → Specification → Discuss (opt) → Architecture → Design (opt) → Implementation → Review
- **AC-3.5:** Given um projeto sem fase de design completada, When Sheldon avança, Then pula design e vai para implementation (porque é opcional)

#### Business Rules

- Model role `designer` recebe opus no perfil balanced (design exige criatividade comparável a architecture)
- A fase de design é listada no phase map com indicador "(opt)" para sinalizar que é opcional
- Sheldon deve perguntar ao usuário se quer executar a fase de design antes de pular

---

## Summary Matrix

| Feature | Priority | Effort | Risk | Functional Reqs | Acceptance Criteria |
|---------|----------|--------|------|-----------------|---------------------|
| F1 — Agent Definition | P0 | M | Baixo | 9 | 4 |
| F2 — Design Workflows | P0 | L | Médio | 8 | 4 |
| F3 — Integration | P1 | S | Baixo | 8 | 5 |

---

## Scope Decisions

### Changes from Original Proposal

O escopo expandiu significativamente em relação à análise do Raj:
- **Adicionado:** Skill completa de Frontend Design (art direction, código production-grade, motion, guardrails anti-genéricos)
- **Adicionado:** Produção de código funcional além de especificações
- **Mantido:** Atomic Design, design tokens, acessibilidade, fase opcional
- **Reduzido:** 1 workflow por track (em vez de 2 como Raj sugeriu inicialmente)

### In Scope

- Agent YAML com persona completa e skill de Frontend Design
- Atomic Design methodology (atoms → pages)
- Art direction explícita com guardrails anti-genéricos
- Design tokens (CSS variables)
- UI specification (layouts, componentes, estados, responsivo)
- Motion design com prefers-reduced-motion
- Acessibilidade (HTML semântico, keyboard nav, contraste, responsivo)
- Código frontend production-grade (componentes, páginas)
- Workflows para 3 tracks
- Integração (teams, Sheldon, schema, model profiles)

### Out of Scope

- Design de marca/branding completo (logo, identidade visual corporativa)
- Ferramentas de design externas (Figma, Sketch) — a agente trabalha com código e markdown
- Testes automatizados de UI (responsabilidade do Howard)
- Design de APIs ou data models (responsabilidade do Leonard)

---

## Next Steps

- [x] Requirements reviewed and approved by the user
- [x] Handoff created for specification phase (penny)
- [ ] State.json updated with status `completed`
