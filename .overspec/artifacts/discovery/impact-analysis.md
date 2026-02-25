# Impact Analysis: overspec-dev

| Field    | Value                |
|----------|----------------------|
| Project  | overspec-dev         |
| Date     | 2026-02-25           |
| Version  | 3.0                  |
| Agent    | raj                  |
| Phase    | Discovery (New Features) |

---

## Feature Overview

Adicionar uma **agente especialista em design** ao OverSpec com expertise em **Atomic Design** — a metodologia que organiza componentes de UI em 5 níveis hierárquicos: atoms, molecules, organisms, templates e pages. A agente será responsável por criar design systems, especificações de UI e design tokens, posicionando-se entre a fase de arquitetura (Leonard) e implementação (Howard).

**Decisões do usuário:**
- Fase de design é **opcional** (como discuss)
- Persona inspirada em personagem do Big Bang Theory (a definir por Penny)
- Sem constraints adicionais

---

## Current Architecture Summary

O OverSpec opera com 7 agentes especializados orquestrados por Sheldon, com 3 tracks de projeto (greenfield, brownfield, new-features). A comunicação é artifact-driven e o state.json controla o progresso. Cada fase tem workflows com 4 arquivos padrão (yaml + instructions + template + checklist).

**Agent roster atual:** Sheldon (orchestrator), Penny (analyst), Leonard (architect), Howard (developer), Amy (reviewer), Raj (analyst), Bernadette (spec designer).

**Model roles definidos:** orchestrator, analyst, architect, developer, reviewer — **não existe "designer"**.

**Gap identificado:** Nenhum agente cobre design visual, UI/UX, design systems ou Atomic Design. Leonard foca em arquitetura de software (componentes, data model, tech stack), não em design de interfaces.

---

## Impact Assessment

### Feature 1: Agent Definition — Design Specialist

| Field | Value |
|-------|-------|
| **Effort** | M |
| **Risk** | Baixo |
| **Priority** | P0 |

**Affected Components:**
- `core/agents/_schema.json` — Adicionar "designer" ao enum model_role
- `overspec.yaml` — Adicionar designer aos 3 model_profiles (quality, balanced, budget)
- `specs/software/spec.yaml` — Registrar o novo agente

**New Components:**
- `core/agents/design-specialist.agent.yaml` — Definição completa da agente (~300 linhas)

**Dependencies:** Nenhuma dependência externa. Usa os mesmos padrões dos agentes existentes.

**Integration Points:**
- Sheldon roteia para a design specialist quando a fase de design é alcançada
- Consome artifacts de Penny (requirements) e Leonard (architecture)
- Produz artifacts consumidos por Howard (implementation) e Amy (review)

**Risk Details:** Risco baixo — criação de agente segue padrão bem estabelecido. Único risco é a persona não capturar bem a expertise em Atomic Design.

**Recommended Approach:** Criar o agent YAML seguindo o padrão de Leonard (architect) como base, adaptando para design. Incluir Atomic Design como framework core na persona e nos princípios.

---

### Feature 2: Design Phase — Workflows para 3 Tracks

| Field | Value |
|-------|-------|
| **Effort** | L |
| **Risk** | Médio |
| **Priority** | P0 |

**Affected Components:**
- `overspec.yaml` — Adicionar fase `design` (order 3.5, optional) nos 3 tracks
- `specs/software/spec.yaml` — Registrar workflows e templates do design
- `core/agents/sheldon.agent.yaml` — Atualizar phase maps para incluir design

**New Components:**
- `core/workflows/3.5-design/workflow.yaml` — Design system (greenfield)
- `core/workflows/3.5-design/instructions.md` — Instruções para greenfield
- `core/workflows/3.5-design/template.md` — Template do design system
- `core/workflows/3.5-design/checklist.md` — Checklist de validação
- `core/workflows/bf-2.5-design/workflow.yaml` — Design audit (brownfield)
- `core/workflows/bf-2.5-design/instructions.md` — Instruções para brownfield
- `core/workflows/bf-2.5-design/template.md` — Template do design audit
- `core/workflows/bf-2.5-design/checklist.md` — Checklist de validação
- `core/workflows/nf-3.5-design/workflow.yaml` — Feature UI design (new-features)
- `core/workflows/nf-3.5-design/instructions.md` — Instruções para new-features
- `core/workflows/nf-3.5-design/template.md` — Template do feature UI
- `core/workflows/nf-3.5-design/checklist.md` — Checklist de validação

**Dependencies:** Feature 1 (agent definition) deve ser feita antes.

**Integration Points:**
- Handoff chain: Leonard → Design Specialist → Howard (nos 3 tracks)
- Amy precisa saber revisar artifacts de design
- State machine já é dinâmica (lê fases do overspec.yaml)

**Risk Details:** Risco médio — 12 novos arquivos de workflow. Principal risco é manter consistência com os workflows existentes. A fase opcional precisa de handling correto no state machine.

**Recommended Approach:** Criar um workflow por track (não dois como sugerido inicialmente). Cada track tem um único workflow de design com escopo adaptado:
- Greenfield: design system completo (Atomic Design + tokens + UI spec)
- Brownfield: audit do design existente + plano de melhoria
- New-features: design da feature integrando ao design system existente

---

### Feature 3: Integration — Teams, Handoffs e Review

| Field | Value |
|-------|-------|
| **Effort** | S |
| **Risk** | Baixo |
| **Priority** | P1 |

**Affected Components:**
- `teams/team-fullstack.yaml` — Adicionar design-specialist
- `teams/team-newfeatures.yaml` — Adicionar design-specialist
- `teams/team-brownfield.yaml` — Adicionar design-specialist
- `core/agents/sheldon.agent.yaml` — Atualizar phase maps visuais

**New Components:**
- `artifacts/design/.gitkeep` — Diretório para artifacts de design

**Dependencies:** Features 1 e 2 devem estar completas.

**Integration Points:**
- Teams passam a incluir a design specialist
- Sheldon mostra a fase de design no phase map
- Amy verifica artifacts de design na review

**Risk Details:** Risco baixo — mudanças de configuração apenas.

**Recommended Approach:** Atualizar os 3 team presets e os phase maps do Sheldon. Não alterar team-quick (quick fix não precisa de design).

---

## Summary Matrix

| Feature | Effort | Risk | Affected Files | New Files |
|---------|--------|------|----------------|-----------|
| Agent Definition | M | Baixo | 3 | 1 |
| Design Workflows (3 tracks) | L | Médio | 3 | 12 |
| Integration (teams, handoffs) | S | Baixo | 4 | 1 |

**Total: ~10 arquivos modificados, ~14 arquivos novos**

---

## Recommendations

1. **Fase opcional:** Implementar design como fase opcional nos 3 tracks (order 3.5 / 2.5), com `required: false` como a fase discuss
2. **Um workflow por track:** Simplificar para 1 workflow de design por track em vez de 2, mantendo foco e reduzindo complexidade
3. **3 artifacts de output:** design-system.md (hierarquia Atomic Design), ui-specification.md (specs de UI), design-tokens.json (tokens programáticos)
4. **Handoff explícito:** Leonard → Design Specialist → Howard, com artifacts de design como input obrigatório de Howard quando a fase de design é executada
5. **Implementar em 3 épicos:** (1) Agent definition + schema, (2) Workflows dos 3 tracks, (3) Integração (teams, Sheldon, artifacts)

---

## Next Steps

- [x] Impact analysis reviewed and approved by the user
- [x] Handoff created for Penny (feature requirements)
- [ ] State.json updated with status `completed`
