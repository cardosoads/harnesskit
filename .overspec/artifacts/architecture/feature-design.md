# Feature Design: overspec-dev

| Field    | Value                         |
|----------|-------------------------------|
| Project  | overspec-dev                  |
| Date     | 2026-02-25                    |
| Version  | 3.0                           |
| Agent    | leonard                       |
| Phase    | Architecture (New Features)   |

---

## Executive Summary

Design para integrar a **Design Specialist** ao OverSpec — uma nova agente com fase opcional de design entre architecture e implementation. A abordagem segue o padrão existente: YAML agent definition + workflows de 4 arquivos + registro em spec/teams/overspec.yaml. O design principal é a agente em si, que combina Atomic Design + Frontend Design skill numa persona coerente. Nenhuma mudança estrutural no framework é necessária — apenas extensão dos patterns existentes.

---

## Existing Architecture Overview

O OverSpec é um framework de orquestração baseado em configuração (YAML/Markdown/JSON). Não há código runtime — tudo são definições que guiam agentes de IA.

**Estrutura atual:**
- 7 agentes definidos em YAML (~150-350 linhas cada)
- 3 tracks com fases dinâmicas (lidas de overspec.yaml)
- Workflows com 4 arquivos padrão (yaml + instructions + template + checklist)
- State machine dinâmica baseada em state.json
- 5 model_roles: orchestrator, analyst, architect, developer, reviewer
- 4 team presets com combinações de agentes

**Padrões que devemos respeitar:**
- Agent YAML segue `_schema.json` (seções: agent, persona, language_protocol, phases, menu, activation, behaviors, outputs, consumes)
- Workflows seguem `workflow-engine.md` (steps com actions: ask, generate, checklist, auto, party)
- Fases opcionais existem como precedente (discuss, order 2.5)

---

## Feature Designs

### Design 1: Agent Definition (US-001, US-002, US-003)

#### Current State

Existem 7 agentes com model_roles fixos. O enum em `_schema.json` tem 5 valores. Não existe agente de design nem role "designer" nos model_profiles. A cadeia de handoff vai direto de Leonard → Howard.

#### Proposed Changes

- `core/agents/_schema.json` — Adicionar `"designer"` ao enum `model_role`
- `overspec.yaml` — Adicionar `designer` aos 3 model_profiles:
  - quality: `"opus"`
  - balanced: `"opus"` (design requer criatividade de alto nível)
  - budget: `"sonnet"`

#### New Components

- `core/agents/design-specialist.agent.yaml` — Definição completa (~350 linhas)

**Estrutura proposta da agente:**

```yaml
agent:
  id: design-specialist
  name: "Emily"               # Emily Sweeney — neuroscientist, artistic
  title: "Design Specialist"
  icon: "🎨"
  version: "1.0.0"
  inspiration: "Emily Sweeney — The Big Bang Theory"
  model_role: "designer"

persona:
  role: >
    Design specialist for OverSpec. Creates design systems using Atomic
    Design methodology, defines art direction, produces design tokens,
    UI specifications, and production-grade frontend code.

  identity: >
    Creative but methodical. Artistic sensibility with engineering
    discipline. Refuses generic "safe" designs — every output has
    intentional art direction with a memorability hook. Believes
    interfaces should have personality, not just function. Respects
    existing code conventions when integrating.

  style: >
    Visual and descriptive. Presents design options with clear
    rationales. Uses structured hierarchy (Atomic Design levels) but
    with creative flair. Shows, doesn't just tell.

  catchphrase: >
    A generic interface is a missed opportunity. Every pixel should
    have a reason to exist.

  principles:
    - "ART DIRECTION FIRST: No 'safe defaults'. Pick an explicit aesthetic."
    - "ATOMIC STRUCTURE: atoms → molecules → organisms → templates → pages"
    - "TOKENS ARE LAW: Colors, typography, spacing — all centralized in tokens"
    - "ACCESSIBILITY IS NON-NEGOTIABLE: Semantic HTML, keyboard nav, contrast"
    - "MOTION WITH RESTRAINT: One orchestrated entrance > many tiny animations"
    - "ANTI-GENERIC: At least one memorability hook per design"
    - "PRODUCTION-GRADE: Runnable code, not pseudo-code"

phases: [design]

menu:
  - trigger: "design-system"
    action: "design-system"
    description: "Create Atomic Design system (atoms → pages)"
  - trigger: "art-direction"
    action: "art-direction"
    description: "Define art direction with named aesthetic"
  - trigger: "tokens"
    action: "design-tokens"
    description: "Create design tokens (CSS variables)"
  - trigger: "ui-spec"
    action: "ui-specification"
    description: "Specify UI: layouts, states, responsive, a11y"
  - trigger: "audit"
    action: "design-audit"
    description: "Audit existing design system (brownfield)"
```

**Activation sequence (6 steps):**
1. Load persona
2. Read overspec.yaml + response_language
3. Read state.json
4. Read input artifacts (architecture/requirements)
5. Monitor context usage (WARNING/CRITICAL thresholds)
6. Present design approach and wait

**Behaviors (5):**
- `design-system`: Full Atomic Design hierarchy
- `ui-specification`: Layouts, componentes, estados, responsivo
- `design-tokens`: CSS variables (cores, tipografia, spacing, efeitos)
- `design-audit`: Brownfield — audit + improvement plan
- `feature-ui`: New-features — design integrado ao sistema existente

**Outputs (3):**
- `artifacts/design/design-system.md` — Hierarquia Atomic Design + componentes
- `artifacts/design/ui-specification.md` — Specs de UI com estados e responsividade
- `artifacts/design/design-tokens.md` — Design tokens documentados

**Consumes:**
- `artifacts/discovery/requirements.md` ou `feature-requirements.md` (de Penny)
- `artifacts/architecture/architecture.md` ou `feature-design.md` (de Leonard)
- `artifacts/discovery/impact-analysis.md` (de Raj, quando disponível)

#### Interface Changes

**Handoff chain atualizada:**
```
Antes:  Leonard → Howard → Amy
Depois: Leonard → Emily (design) → Howard → Amy
```

A fase de design é opcional. Quando skipped, a chain continua como antes (Leonard → Howard).

#### Data Flow

```
Penny (requirements/stories)
    ↓
Leonard (architecture/feature-design)
    ↓
Emily (design-system + ui-spec + tokens)  [OPTIONAL]
    ↓
Howard (implementation — consome artifacts de design quando existem)
    ↓
Amy (review — verifica design artifacts se foram produzidos)
```

#### Trade-offs

| Option | Pros | Cons | Chosen? |
|--------|------|------|---------|
| Emily Sweeney como persona | Personagem artístico, encaixa bem com design; neuroscientista = metódica + criativa | Menos conhecida que outros personagens | **Sim** |
| Stuart Bloom como persona | Dono de loja de quadrinhos, artista | Personagem cômico demais, pouca autoridade técnica | Não |
| Persona não-TBBT | Liberdade total | Quebra o tema do roster | Não |

| Option | Pros | Cons | Chosen? |
|--------|------|------|---------|
| 3 artifacts separados (system + spec + tokens) | Granularidade, cada um serve um propósito | Mais arquivos para gerenciar | **Sim** |
| 1 artifact monolítico | Simples | Muito grande, difícil de revisar parcialmente | Não |

#### Implementation Order
1. Adicionar "designer" ao schema e model_profiles (US-001)
2. Criar design-specialist.agent.yaml (US-002)
3. Definir outputs/consumes no agent YAML (US-003 — junto com US-002)

---

### Design 2: Design Workflows (US-004, US-005, US-006)

#### Current State

Existem 15 diretórios de workflow. Cada track tem seu conjunto. A fase de design não existe em nenhum track. O padrão é consolidado: 4 arquivos por workflow.

#### Proposed Changes

- Nenhuma mudança em workflows existentes

#### New Components

- `core/workflows/3.5-design/` — Greenfield design workflow (4 arquivos)
- `core/workflows/bf-2.5-design/` — Brownfield design audit (4 arquivos)
- `core/workflows/nf-3.5-design/` — New-features design (4 arquivos)

#### Workflow Design: Greenfield (3.5-design)

```yaml
workflow:
  id: design-system
  name: "Design System — Atomic Design & Art Direction"
  phase: design
  agent: design-specialist
  required: false  # Phase is optional

  inputs:
    - "artifacts/architecture/architecture.md"
    - "artifacts/architecture/tech-stack.md"
    - "artifacts/discovery/requirements.md"
    - "artifacts/specification/user-stories.md"

  output:
    path: "artifacts/design/design-system.md"
    handoff_to: [howard]

  steps:
    - id: "brief"
      action: "ask"
      prompt: "Vou criar o design system. Preciso entender: propósito, usuário-alvo, ação primária, densidade de conteúdo, constraints (framework, dark/light, a11y)."
      required: true

    - id: "art-direction"
      action: "generate"
      description: "Definir art direction explícita com nome, rationale e 3 motifs assinatura. Apresentar 2-3 opções quando requisitos são fracos."

    - id: "design-tokens"
      action: "generate"
      description: "Criar design tokens: cores, tipografia (display + body), type scale, spacing scale, efeitos (shadows, borders, radius)."

    - id: "components"
      action: "generate"
      description: "Definir hierarquia Atomic Design: atoms, molecules, organisms, templates, pages. Incluir estados (hover, active, focus-visible, disabled, loading, empty)."

    - id: "motion-a11y"
      action: "generate"
      description: "Motion pass (entrada orquestrada, prefers-reduced-motion) e accessibility gates (HTML semântico, keyboard nav, contraste, responsivo)."

    - id: "generate"
      action: "generate"
      save_to: "artifacts/design/design-system.md"

    - id: "validate"
      action: "checklist"
      checklist: "checklist.md"
```

#### Workflow Design: Brownfield (bf-2.5-design)

```yaml
workflow:
  id: design-audit
  name: "Design Audit & Improvement"
  phase: design
  agent: design-specialist
  required: false

  inputs:
    - "artifacts/analysis/codebase-analysis.md"
    - "artifacts/planning/improvement-plan.md"

  output:
    path: "artifacts/design/design-audit.md"
    handoff_to: [howard]

  steps:
    - id: "scan-existing"
      action: "generate"
      description: "Auditar o design existente: tokens, componentes, consistência, acessibilidade."

    - id: "gaps"
      action: "generate"
      description: "Identificar gaps e inconsistências no design atual."

    - id: "improvement-plan"
      action: "generate"
      description: "Plano de melhoria incremental com design tokens para padronizar."

    - id: "generate"
      action: "generate"
      save_to: "artifacts/design/design-audit.md"

    - id: "validate"
      action: "checklist"
      checklist: "checklist.md"
```

#### Workflow Design: New-Features (nf-3.5-design)

```yaml
workflow:
  id: feature-ui-design
  name: "Feature UI Design"
  phase: design
  agent: design-specialist
  required: false

  inputs:
    - "artifacts/architecture/feature-design.md"
    - "artifacts/specification/feature-stories.md"
    - "artifacts/discovery/impact-analysis.md"

  output:
    path: "artifacts/design/feature-ui.md"
    handoff_to: [howard]

  steps:
    - id: "context"
      action: "generate"
      description: "Analisar design system existente (se houver). Se não houver, criar mínimo viável."

    - id: "feature-design"
      action: "generate"
      description: "Design da feature: art direction, tokens, componentes novos, UI specification."

    - id: "integration"
      action: "generate"
      description: "Plano de integração com design system existente ou extensão dos tokens."

    - id: "generate"
      action: "generate"
      save_to: "artifacts/design/feature-ui.md"

    - id: "validate"
      action: "checklist"
      checklist: "checklist.md"
```

#### Trade-offs

| Option | Pros | Cons | Chosen? |
|--------|------|------|---------|
| 1 workflow por track | Simples, foco claro | Workflow greenfield pode ficar grande | **Sim** |
| 2 workflows por track (system + spec) | Granularidade | Mais complexidade, 24 arquivos em vez de 12 | Não |

#### Implementation Order
1. Workflow greenfield — 3.5-design/ (US-004)
2. Workflow brownfield — bf-2.5-design/ (US-005)
3. Workflow new-features — nf-3.5-design/ (US-006)

---

### Design 3: Integration (US-007 a US-012)

#### Current State

3 tracks com fases configuradas em overspec.yaml. 4 team presets. Sheldon tem phase maps para 3 tracks. State machine dinâmica.

#### Proposed Changes

- `overspec.yaml` — Adicionar fase `design` nos 3 tracks:
  ```yaml
  greenfield_phases:
    design:
      enabled: true
      required: false
      order: 3.5
  brownfield_phases:
    design:
      enabled: true
      required: false
      order: 2.5
  newfeatures_phases:
    design:
      enabled: true
      required: false
      order: 3.5
  ```
- `teams/team-fullstack.yaml` — Adicionar `design-specialist` entre leonard e howard
- `teams/team-newfeatures.yaml` — Adicionar `design-specialist` entre leonard e howard
- `teams/team-brownfield.yaml` — Adicionar `design-specialist` entre raj e howard
- `core/agents/sheldon.agent.yaml` — Atualizar phase maps (3 blocos) e new_project_detection
- `specs/software/spec.yaml` — Registrar agente + 3 workflows + 3 templates
- `core/engine/state-machine.md` — Adicionar documentação sobre fases opcionais (required: false → Sheldon pergunta antes de pular)

#### New Components

- `artifacts/design/.gitkeep` — Já criado

#### Trade-offs

| Option | Pros | Cons | Chosen? |
|--------|------|------|---------|
| Design optional em todos os tracks | Flexibilidade máxima | Usuário pode não saber quando precisa de design | **Sim** |
| Design required em greenfield, optional em brownfield/new-features | Garante design em projetos novos | Projetos simples sem UI teriam overhead | Não |

#### Implementation Order
1. overspec.yaml — fases + model profiles (US-001 parcial + US-007)
2. Teams — 3 presets (US-008)
3. spec.yaml — registro (US-009)
4. Sheldon — phase maps e detection (US-010)
5. artifacts/design — confirmar diretório (US-011)
6. state-machine.md — documentar fases opcionais (US-012)

---

## Implementation Plan for Howard

| Order | Story | What to Build | Effort |
|-------|-------|---------------|--------|
| 1 | US-001 | Adicionar "designer" ao _schema.json + model_profiles no overspec.yaml | S |
| 2 | US-002 + US-003 | Criar design-specialist.agent.yaml completo (persona Emily, skill Frontend Design, activation, behaviors, outputs, consumes) | L |
| 3 | US-007 | Adicionar fase design (required: false) nos 3 tracks do overspec.yaml | S |
| 4 | US-004 | Criar workflow greenfield 3.5-design/ (4 arquivos) | L |
| 5 | US-005 | Criar workflow brownfield bf-2.5-design/ (4 arquivos) | M |
| 6 | US-006 | Criar workflow new-features nf-3.5-design/ (4 arquivos) | M |
| 7 | US-009 | Registrar agente e workflows em spec.yaml | S |
| 8 | US-008 | Atualizar 3 team presets | S |
| 9 | US-010 | Atualizar phase maps e detection do Sheldon | S |
| 10 | US-011 | Confirmar diretório artifacts/design/ | S |
| 11 | US-012 | Documentar fases opcionais no state-machine.md | S |

**Epics sugeridos:**
- **Epic 1 (Foundation):** US-001, US-002+003, US-007 — schema, agente, fases
- **Epic 2 (Workflows):** US-004, US-005, US-006 — 3 workflows
- **Epic 3 (Integration):** US-009, US-008, US-010, US-011, US-012 — registro, teams, Sheldon, docs

---

## Next Steps

- [x] Design reviewed and approved by the user
- [ ] Handoff created for Howard (implementation)
- [ ] State.json updated with status `completed`
