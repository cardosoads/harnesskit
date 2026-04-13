# Feature Stories: Visual CLI Enhancement

| Field    | Value                          |
|----------|--------------------------------|
| Project  | harnesskit-dev                   |
| Date     | 2026-02-25                     |
| Version  | 4.0                            |
| Agent    | penny                          |
| Phase    | Specification (New Features)   |
| Cycle    | 4                              |

---

## Executive Summary

User stories para a **melhoria visual completa** do framework Harnesskit para ambiente CLI com Markdown rendering. Organizadas em 3 epics (Foundation, Application, Advanced) com 15 stories cobrindo style guide, callouts, progress bars, Mermaid diagrams e agent formatting enhancement.

**Total Stories:** 15
- Must Have: 11
- Should Have: 3
- Could Have: 1

---

## User Stories by Feature

### Epic 1 — Foundation (Style Guide)

#### US-001 — Criar Visual Style Guide

**As a** framework maintainer,
**I want to** ter um documento centralizado com todos os padrões visuais,
**So that** todos os agentes formatem output de forma consistente.

**Acceptance Criteria:**
1. Given o arquivo `core/style-guide.md` existe, When lido, Then define os 6 tipos de callouts com emoji + formato
2. Given o style guide é consultado, When progress bars são buscadas, Then encontra formato `████████░░ 80% (4/5)` com regras de uso
3. Given o style guide é consultado, When Mermaid é buscado, Then encontra exemplos dos 3 tipos (flowchart, sequence, class/ER)
4. Given o style guide é consultado, When emphasis patterns são buscados, Then encontra regras para bold, italic, code, strikethrough
5. Given o style guide é consultado, When anti-patterns são buscados, Then encontra pelo menos 5 exemplos do que NÃO fazer

**Technical Notes:** Máximo ~200 linhas. Exemplos copy-pasteable. Referenciado por todos os agents.
**Priority:** Must
**Effort:** M

---

### Epic 2 — Application (Callouts, Progress, Agent Enhancement)

#### US-002 — Aplicar callouts em instructions.md (greenfield)

**As a** agent following greenfield workflows,
**I want to** que instructions tenham callouts visuais nos pontos críticos,
**So that** regras importantes, warnings e tips sejam visualmente destacados.

**Acceptance Criteria:**
1. Given cada instructions.md do greenfield é lido, When regras críticas existem, Then usam `> 📋 **Important:**`
2. Given cada instructions.md do greenfield é lido, When há riscos ou cuidados, Then usam `> ⚠️ **Warning:**`
3. Given callouts antigos (formato `> IMPORTANT:`) existem, When migrados, Then usam o novo formato padronizado
4. Given cada arquivo é contado, When callouts são somados, Then nenhum tem mais de 5

**Technical Notes:** 7 instructions.md no greenfield track. Mudanças aditivas — conteúdo existente preservado.
**Priority:** Must
**Effort:** M

---

#### US-003 — Aplicar callouts em instructions.md (brownfield)

**As a** agent following brownfield workflows,
**I want to** que instructions tenham callouts padronizados,
**So that** a experiência visual seja consistente entre tracks.

**Acceptance Criteria:**
1. Given cada instructions.md do brownfield é lido, When regras críticas existem, Then usam callouts padronizados
2. Given o formato é comparado com greenfield, When analisado, Then usa os mesmos padrões de callout

**Technical Notes:** 4 instructions.md no brownfield track.
**Priority:** Must
**Effort:** S

---

#### US-004 — Aplicar callouts em instructions.md (new-features)

**As a** agent following new-features workflows,
**I want to** que instructions tenham callouts padronizados,
**So that** a experiência visual seja consistente entre tracks.

**Acceptance Criteria:**
1. Given cada instructions.md do new-features é lido, When regras críticas existem, Then usam callouts padronizados
2. Given o formato é comparado com greenfield, When analisado, Then usa os mesmos padrões de callout

**Technical Notes:** 4 instructions.md no new-features track. Inclui nf-1-discovery (2 workflows), nf-2-specification, nf-3-architecture, nf-3.5-design, nf-4-implementation.
**Priority:** Must
**Effort:** S

---

#### US-005 — Aplicar callouts em template.md (todos os tracks)

**As a** agent producing artifacts,
**I want to** que templates tenham callouts contextuais,
**So that** notas e orientações sejam visualmente destacadas nos artefatos.

**Acceptance Criteria:**
1. Given cada template.md é lido, When contém notas como "preenchido automaticamente", Then usa `> 📌 **Note:**`
2. Given cada template.md é lido, When contém orientação de preenchimento, Then usa `> 💡 **Tip:**`
3. Given callouts são contados por template, When somados, Then nenhum tem mais de 4

**Technical Notes:** ~16 template.md files. Callouts são supplementary — não alteram estrutura do template.
**Priority:** Should
**Effort:** M

---

#### US-006 — Adicionar progress bars ao Sheldon (status)

**As a** user checking project status,
**I want to** ver progress bars visuais no status do Sheldon,
**So that** o progresso seja imediatamente visível.

**Acceptance Criteria:**
1. Given Sheldon apresenta status, When o projeto está 60% completo, Then mostra `██████░░░░ 60% (3/5 phases)`
2. Given Sheldon apresenta status detalhado, When uma fase tem 3/5 steps, Then mostra `██████░░░░ 60% (3/5 steps)`
3. Given a progress bar é renderizada, When medida, Then tem largura fixa de 10 chars

**Technical Notes:** Atualizar `activation` > "Present visual status" no sheldon.agent.yaml. Usar `█` (U+2588) e `░` (U+2591).
**Priority:** Must
**Effort:** S

---

#### US-007 — Adicionar progress/compliance bar à Amy (review)

**As a** reviewer generating a report,
**I want to** mostrar uma compliance bar no review report,
**So that** o resultado da review seja visualmente imediato.

**Acceptance Criteria:**
1. Given Amy gera review report, When 14/14 items passam, Then mostra `██████████ 100% (14/14 passed)`
2. Given Amy gera review report, When 10/14 items passam, Then mostra `███████░░░ 71% (10/14 passed)`
3. Given a review template é lida, When compliance bar é buscada, Then existe seção dedicada

**Technical Notes:** Atualizar `5-review/template.md` e `amy.agent.yaml` (style section).
**Priority:** Must
**Effort:** S

---

#### US-008 — Enriquecer persona.style do Sheldon

**As a** Sheldon (orchestrator),
**I want to** ter formatting directives específicas na minha persona,
**So that** meu output seja visualmente rico e consistente.

**Acceptance Criteria:**
1. Given sheldon.agent.yaml é lido, When `persona.style` é inspecionado, Then referencia `core/style-guide.md`
2. Given sheldon.agent.yaml é lido, When `persona.style` é inspecionado, Then menciona progress bars, callouts `📋 Important` para Constitution principles
3. Given Sheldon apresenta status, When callouts são usados, Then segue o padrão do style guide

**Technical Notes:** Adicionar ~3-5 linhas ao `persona.style` existente.
**Priority:** Must
**Effort:** S

---

#### US-009 — Enriquecer persona.style de Penny, Howard e Raj

**As a** framework maintainer,
**I want to** que Penny, Howard e Raj tenham formatting directives,
**So that** cada agente formate output de forma rica e consistente.

**Acceptance Criteria:**
1. Given penny.agent.yaml é lido, When `persona.style` é inspecionado, Then referencia style guide e menciona callouts `💡 Tip`, tabelas de summary
2. Given howard.agent.yaml é lido, When `persona.style` é inspecionado, Then referencia style guide e menciona code blocks com syntax highlighting, file trees
3. Given raj.agent.yaml é lido, When `persona.style` é inspecionado, Then referencia style guide e menciona impact matrices, risk callouts `⚠️ Warning`

**Technical Notes:** Adicionar ~3-5 linhas ao `persona.style` existente de cada agente.
**Priority:** Must
**Effort:** S

---

#### US-010 — Enriquecer persona.style de Leonard, Amy e Emily

**As a** framework maintainer,
**I want to** que Leonard, Amy e Emily tenham formatting directives,
**So that** cada agente formate output de forma rica e consistente.

**Acceptance Criteria:**
1. Given leonard.agent.yaml é lido, When `persona.style` é inspecionado, Then referencia style guide e menciona Mermaid diagrams, trade-off tables
2. Given amy.agent.yaml é lido, When `persona.style` é inspecionado, Then referencia style guide e menciona compliance bars, severity indicators (🔴🟡🟢)
3. Given design-specialist.agent.yaml é lido, When `persona.style` é inspecionado, Then referencia style guide e menciona design token code blocks, component state tables

**Technical Notes:** Adicionar ~3-5 linhas ao `persona.style` existente de cada agente.
**Priority:** Must
**Effort:** S

---

### Epic 3 — Advanced (Mermaid Diagrams)

#### US-011 — Adicionar Mermaid ao template de architecture (greenfield)

**As a** Leonard designing architecture,
**I want to** ter seções de Mermaid diagram no template de architecture,
**So that** componentes e data flow sejam visualizados graficamente.

**Acceptance Criteria:**
1. Given `3-architecture/template.md` é lido, When a seção Component Diagram é inspecionada, Then contém Mermaid flowchart placeholder com Handlebars
2. Given o diagrama Mermaid é renderizado, When lido, Then mostra componentes e suas conexões
3. Given o terminal não suporta Mermaid, When o output é lido, Then existe texto descritivo como fallback antes do diagrama

**Technical Notes:** Substituir placeholder ASCII art por Mermaid flowchart. Manter texto descritivo como fallback.
**Priority:** Should
**Effort:** M

---

#### US-012 — Adicionar Mermaid aos templates de architecture (brownfield + new-features)

**As a** Leonard/Raj designing changes,
**I want to** ter Mermaid diagrams nos templates de brownfield e new-features,
**So that** a visualização gráfica seja consistente entre tracks.

**Acceptance Criteria:**
1. Given `bf-2-planning/template.md` é lido, When seção de diagrama é buscada, Then contém Mermaid placeholder
2. Given `nf-3-architecture/template.md` é lido, When seção de diagrama é buscada, Then contém Mermaid placeholder
3. Given cada diagrama tem fallback texto, When Mermaid não renderiza, Then a informação não é perdida

**Technical Notes:** Adaptar o padrão de US-011 para os outros tracks.
**Priority:** Should
**Effort:** S

---

#### US-013 — Adicionar Mermaid guidance ao Leonard

**As a** Leonard (architect),
**I want to** ter orientação no meu agent.yaml sobre como usar Mermaid,
**So that** eu gere diagramas consistentes e úteis.

**Acceptance Criteria:**
1. Given leonard.agent.yaml é lido, When `persona.style` é inspecionado, Then menciona Mermaid diagrams como ferramenta esperada
2. Given instructions de architecture são lidas, When Mermaid é buscado, Then encontra orientação sobre quando e como usar

**Technical Notes:** Complementa US-010 com orientação mais detalhada no instructions.md de architecture.
**Priority:** Must
**Effort:** S

---

#### US-014 — Adicionar Mermaid workflow pipeline ao Sheldon

**As a** Sheldon (orchestrator),
**I want to** poder mostrar o workflow pipeline como Mermaid flowchart,
**So that** o usuário visualize o fluxo de fases graficamente.

**Acceptance Criteria:**
1. Given Sheldon usa o comando "map", When o mapa é apresentado, Then inclui opcionalmente um Mermaid flowchart do pipeline
2. Given o flowchart é renderizado, When as fases são mostradas, Then indica visualmente a fase atual com styling

**Technical Notes:** Adicionar na seção `show-map` do sheldon.agent.yaml. Mermaid é supplementary — o mapa texto continua existindo.
**Priority:** Could
**Effort:** S

---

#### US-015 — Atualizar party-mode instructions com callouts

**As a** Sheldon moderating party mode,
**I want to** que party-mode/instructions.md use callouts padronizados,
**So that** a experiência visual seja consistente com o resto do framework.

**Acceptance Criteria:**
1. Given party-mode/instructions.md é lido, When regras de moderação existem, Then usam callouts padronizados
2. Given o formato é comparado com outros instructions, When analisado, Then usa os mesmos padrões

**Technical Notes:** 1 arquivo. Inclui formatação de agent roster e discussion rules.
**Priority:** Must
**Effort:** S

---

## Story Summary

| ID | Story | Epic | Priority | Effort |
|----|-------|------|----------|--------|
| US-001 | Criar Visual Style Guide | 1 — Foundation | Must | M |
| US-002 | Callouts instructions greenfield (7 files) | 2 — Application | Must | M |
| US-003 | Callouts instructions brownfield (4 files) | 2 — Application | Must | S |
| US-004 | Callouts instructions new-features (4+ files) | 2 — Application | Must | S |
| US-005 | Callouts templates (todos os tracks, ~16 files) | 2 — Application | Should | M |
| US-006 | Progress bars Sheldon (status) | 2 — Application | Must | S |
| US-007 | Compliance bar Amy (review) | 2 — Application | Must | S |
| US-008 | Enriquecer persona.style Sheldon | 2 — Application | Must | S |
| US-009 | Enriquecer persona.style Penny, Howard, Raj | 2 — Application | Must | S |
| US-010 | Enriquecer persona.style Leonard, Amy, Emily | 2 — Application | Must | S |
| US-011 | Mermaid template architecture greenfield | 3 — Advanced | Should | M |
| US-012 | Mermaid templates brownfield + new-features | 3 — Advanced | Should | S |
| US-013 | Mermaid guidance Leonard (agent + instructions) | 3 — Advanced | Must | S |
| US-014 | Mermaid workflow pipeline Sheldon | 3 — Advanced | Could | S |
| US-015 | Callouts party-mode instructions | 2 — Application | Must | S |

---

## Implementation Order (Recommendation for Leonard)

1. **US-001** primeiro — style guide fundamenta tudo
2. **US-008, US-009, US-010** — agent formatting (aplica style guide)
3. **US-006, US-007** — progress bars (self-contained)
4. **US-002, US-003, US-004, US-015** — callouts em instructions
5. **US-005** — callouts em templates
6. **US-013, US-011, US-012** — Mermaid (Leonard + templates)
7. **US-014** — Mermaid Sheldon (last, lowest priority)

---

## Next Steps

- [x] Stories reviewed and approved by the user
- [ ] Handoff to Leonard (architecture / feature design)
- [ ] State.json updated
