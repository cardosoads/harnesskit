# Feature Stories: overspec-dev

| Field    | Value                          |
|----------|--------------------------------|
| Project  | overspec-dev                   |
| Date     | 2026-02-25                     |
| Version  | 3.0                            |
| Agent    | penny                          |
| Phase    | Specification (New Features)   |

---

## Executive Summary

User stories para adicionar a **Design Specialist** ao OverSpec — uma agente completa de design com Atomic Design, art direction, design tokens, UI specification, motion, acessibilidade e código frontend production-grade. Organizadas em 3 features (agent, workflows, integration) com 12 stories.

**Total Stories:** 12
- Must Have: 9
- Should Have: 2
- Could Have: 1

---

## User Stories by Feature

### Feature: F1 — Agent Definition

#### US-001 — Adicionar model_role "designer" ao schema

**As a** framework maintainer,
**I want to** ter o role "designer" disponível no agent schema,
**So that** a design specialist possa ser validada corretamente.

**Acceptance Criteria:**
1. Given `_schema.json` é lido, When o campo model_role é inspecionado, Then o enum inclui "designer"
2. Given overspec.yaml é lido, When model_profiles são inspecionados, Then cada profile (quality, balanced, budget) tem o role "designer" com modelo definido

**Technical Notes:** Raj identificou que o enum model_role tem 5 valores; adicionar "designer" como 6º. Em model_profiles: quality=opus, balanced=opus, budget=sonnet.
**Priority:** Must
**Effort:** S

---

#### US-002 — Criar design-specialist.agent.yaml

**As a** framework maintainer,
**I want to** ter uma agente de design com persona completa,
**So that** o OverSpec possa guiar design de interfaces com Atomic Design e art direction.

**Acceptance Criteria:**
1. Given o arquivo `design-specialist.agent.yaml` existe, When validado contra `_schema.json`, Then passa sem erros e contém todas as seções obrigatórias (agent, persona, phases, menu, activation, behaviors, outputs, consumes)
2. Given a agente é descrita, When sua persona é lida, Then inclui princípios de Atomic Design, art direction anti-genérica e frontend production-grade
3. Given a agente tem behaviors, When listados, Then incluem: design-system, ui-specification, design-tokens, design-audit, feature-ui
4. Given a agente tem activation, When a sequence é executada, Then inclui context monitoring (como os outros specialists)

**Technical Notes:** Base na estrutura de leonard.agent.yaml. Persona inspirada em personagem do Big Bang Theory. Incluir a skill completa de Frontend Design como referência nos princípios e behaviors. phases: [design].
**Priority:** Must
**Effort:** L

---

#### US-003 — Definir outputs e consumes da design specialist

**As a** framework maintainer,
**I want to** que a agente tenha inputs/outputs claros,
**So that** a cadeia de handoff funcione corretamente.

**Acceptance Criteria:**
1. Given a agente produz outputs, When listados, Then incluem: design-system.md, ui-specification.md, design-tokens.md (todos em artifacts/design/)
2. Given a agente consome artifacts, When listados, Then incluem: requirements ou feature-requirements (de Penny), architecture ou feature-design (de Leonard), impact-analysis (de Raj, quando disponível)
3. Given Howard lê os consumes, When os artifacts de design são listados, Then ele sabe exatamente o que consumir

**Technical Notes:** Handoff chain: Leonard → Design Specialist → Howard. Amy também consome os artifacts de design para review.
**Priority:** Must
**Effort:** S

---

### Feature: F2 — Design Workflows

#### US-004 — Criar workflow de design greenfield (3.5-design)

**As a** design specialist operando num projeto greenfield,
**I want to** ter um workflow que me guie na criação de um design system completo,
**So that** o output seja consistente e production-grade.

**Acceptance Criteria:**
1. Given o diretório `3.5-design/` existe, When inspecionado, Then contém 4 arquivos: workflow.yaml, instructions.md, template.md, checklist.md
2. Given o workflow.yaml é lido, When os steps são listados, Then seguem o fluxo: brief → art-direction → design-tokens → components → motion → accessibility → generate → validate
3. Given o instructions.md é lido, When o conteúdo é analisado, Then cobre Atomic Design completo (atoms → pages), art direction com guardrails anti-genéricos, design tokens (CSS variables), motion com prefers-reduced-motion, e accessibility gates (HTML semântico, keyboard nav, contraste, responsivo)
4. Given o workflow é executado, When a agente conclui, Then produz artifacts em artifacts/design/ e faz handoff para howard

**Technical Notes:** Input: artifacts de Leonard (architecture.md, tech-stack.md) e Penny (requirements.md, user-stories.md). Output: artifacts/design/design-system.md. Este é o workflow mais completo — cria o design system do zero.
**Priority:** Must
**Effort:** L

---

#### US-005 — Criar workflow de design brownfield (bf-2.5-design)

**As a** design specialist operando num projeto brownfield,
**I want to** ter um workflow para auditar e melhorar o design existente,
**So that** o design system seja padronizado incrementalmente.

**Acceptance Criteria:**
1. Given o diretório `bf-2.5-design/` existe, When inspecionado, Then contém 4 arquivos padrão
2. Given o workflow é executado, When a agente analisa, Then audita o design existente antes de propor mudanças
3. Given o instructions.md é lido, When o tom é analisado, Then enfatiza evolução incremental (não rewrite completo)
4. Given o output é gerado, When o artifact é lido, Then contém: audit do estado atual, gaps identificados, design tokens para padronizar, plano de melhoria

**Technical Notes:** Input: codebase-analysis.md (de Raj) e improvement-plan.md. Output: artifacts/design/design-audit.md. Handoff para howard.
**Priority:** Must
**Effort:** M

---

#### US-006 — Criar workflow de design new-features (nf-3.5-design)

**As a** design specialist operando num projeto new-features,
**I want to** ter um workflow para design de features específicas,
**So that** as novas features integrem com o design system existente.

**Acceptance Criteria:**
1. Given o diretório `nf-3.5-design/` existe, When inspecionado, Then contém 4 arquivos padrão
2. Given o workflow é executado, When um design system prévio existe, Then a agente integra a feature nele
3. Given o workflow é executado, When NÃO existe design system prévio, Then a agente cria um mínimo viável
4. Given o output é gerado, When o artifact é lido, Then contém: UI spec da feature, componentes novos (com código), tokens novos ou extensões

**Technical Notes:** Input: feature-design.md (de Leonard) e feature-stories.md (de Penny). Output: artifacts/design/feature-ui.md. Handoff para howard.
**Priority:** Must
**Effort:** M

---

### Feature: F3 — Integration

#### US-007 — Adicionar fase design nos 3 tracks do overspec.yaml

**As a** Sheldon (orchestrator),
**I want to** que a fase design exista como opcional nos 3 tracks,
**So that** o state machine reconheça e possa pular ou executar a fase.

**Acceptance Criteria:**
1. Given overspec.yaml é lido, When greenfield_phases é inspecionado, Then contém `design` com order 3.5 e required: false
2. Given overspec.yaml é lido, When brownfield_phases é inspecionado, Then contém `design` com order 2.5 e required: false
3. Given overspec.yaml é lido, When newfeatures_phases é inspecionado, Then contém `design` com order 3.5 e required: false
4. Given a fase design é optional, When o state machine processa, Then pergunta ao usuário se quer executar antes de pular

**Technical Notes:** O state machine já é dinâmico (lê fases do overspec.yaml), então adicionar a fase é transparente. A questão é o handling de "optional" — como discuss. Pode precisar de atualização no state-machine.md para documentar fases opcionais.
**Priority:** Must
**Effort:** S

---

#### US-008 — Atualizar teams para incluir design-specialist

**As a** framework maintainer,
**I want to** que os 3 team presets principais incluam a design specialist,
**So that** a agente esteja disponível quando o projeto tem UI.

**Acceptance Criteria:**
1. Given team-fullstack.yaml é lido, When os agentes são listados, Then inclui design-specialist
2. Given team-newfeatures.yaml é lido, When os agentes são listados, Then inclui design-specialist
3. Given team-brownfield.yaml é lido, When os agentes são listados, Then inclui design-specialist
4. Given team-quick.yaml é lido, When os agentes são listados, Then NÃO inclui design-specialist

**Technical Notes:** Inserir design-specialist na posição correta (entre leonard e howard na lista).
**Priority:** Must
**Effort:** S

---

#### US-009 — Registrar agente e workflows em spec.yaml

**As a** framework maintainer,
**I want to** que spec.yaml liste o novo agente e todos os workflows de design,
**So that** o framework reconheça os novos recursos.

**Acceptance Criteria:**
1. Given spec.yaml é lido, When components.agents é inspecionado, Then inclui design-specialist.agent.yaml
2. Given spec.yaml é lido, When components.workflows é inspecionado, Then cada track lista o workflow de design correspondente
3. Given spec.yaml é lido, When components.templates é inspecionado, Then cada track lista o template de design correspondente

**Technical Notes:** Seguir o padrão dos registros existentes.
**Priority:** Must
**Effort:** S

---

#### US-010 — Atualizar phase maps do Sheldon

**As a** Sheldon,
**I want to** mostrar a fase de design nos phase maps visuais,
**So that** o usuário veja a fase opcional de design no mapa do projeto.

**Acceptance Criteria:**
1. Given Sheldon apresenta o phase map greenfield, When renderizado, Then mostra: Discovery → Specification → Discuss (opt) → Architecture → Design (opt) → Implementation → Review
2. Given Sheldon apresenta o phase map brownfield, When renderizado, Then mostra: Analysis → Planning → Design (opt) → Implementation → Review
3. Given Sheldon apresenta o phase map new-features, When renderizado, Then mostra: Discovery → Specification → Architecture → Design (opt) → Implementation → Review
4. Given Sheldon detecta um novo projeto, When explica as fases, Then menciona a design specialist e a fase opcional

**Technical Notes:** Atualizar sheldon.agent.yaml nos 3 blocos de phase map e no new_project_detection.
**Priority:** Should
**Effort:** S

---

#### US-011 — Criar diretório de artifacts de design

**As a** design specialist,
**I want to** que o diretório `artifacts/design/` exista,
**So that** meus outputs tenham onde ser salvos.

**Acceptance Criteria:**
1. Given o diretório `artifacts/design/` é verificado, When inspecionado, Then existe com `.gitkeep`
2. Given um workflow de design é executado, When o output é salvo, Then o path `artifacts/design/` é válido

**Technical Notes:** Já criado durante a análise de impacto do Raj. Confirmar que existe.
**Priority:** Should
**Effort:** S

---

#### US-012 — Documentar handling de fases opcionais no state-machine.md

**As a** framework maintainer,
**I want to** que o state-machine.md documente como fases opcionais funcionam,
**So that** fases como discuss e design tenham comportamento previsível.

**Acceptance Criteria:**
1. Given state-machine.md é lido, When a seção de fases opcionais é buscada, Then existe documentação sobre como o orchestrator deve lidar com fases `required: false`
2. Given uma fase é optional, When o state machine processa a transição, Then a instrução diz: "Se a fase tem required: false, pergunte ao usuário se deseja executá-la antes de pular para a próxima"

**Technical Notes:** Atualmente discuss já é opcional mas o handling não está documentado no state-machine.md. Esta story corrige essa lacuna para discuss E design.
**Priority:** Could
**Effort:** S

---

## Story Summary

| ID | Story | Feature | Priority | Effort |
|----|-------|---------|----------|--------|
| US-001 | Adicionar model_role "designer" ao schema | F1 — Agent | Must | S |
| US-002 | Criar design-specialist.agent.yaml | F1 — Agent | Must | L |
| US-003 | Definir outputs e consumes | F1 — Agent | Must | S |
| US-004 | Workflow greenfield (3.5-design) | F2 — Workflows | Must | L |
| US-005 | Workflow brownfield (bf-2.5-design) | F2 — Workflows | Must | M |
| US-006 | Workflow new-features (nf-3.5-design) | F2 — Workflows | Must | M |
| US-007 | Adicionar fase design nos 3 tracks | F3 — Integration | Must | S |
| US-008 | Atualizar teams | F3 — Integration | Must | S |
| US-009 | Registrar em spec.yaml | F3 — Integration | Must | S |
| US-010 | Atualizar phase maps do Sheldon | F3 — Integration | Should | S |
| US-011 | Criar diretório artifacts/design | F3 — Integration | Should | S |
| US-012 | Documentar fases opcionais no state-machine | F3 — Integration | Could | S |

---

## Next Steps

- [x] Stories reviewed and approved by the user
- [ ] Handoff created for Leonard (architecture)
- [ ] State.json updated with status `completed`
