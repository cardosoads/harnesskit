# Impact Analysis: Visual CLI Enhancement

| Field    | Value                          |
|----------|--------------------------------|
| Project  | overharness-dev                   |
| Date     | 2026-02-25                     |
| Version  | 4.0                            |
| Agent    | raj                            |
| Phase    | Discovery (New Features)       |
| Cycle    | 4                              |

---

## Feature Overview

Melhoria visual completa do framework OverHarness para ambiente CLI com suporte a Markdown rendering (Claude Code). O framework atual usa formatação básica — emojis de status, tabelas simples, headers. O objetivo é enriquecer a apresentação visual com progress bars, callouts/admonitions, diagramas Mermaid e formatação mais sofisticada, tanto nas respostas dos agentes quanto nos templates de artefatos.

**Decisões do usuário:**
- Escopo: apresentação dos agentes **e** templates de artefatos
- Ambiente: terminal com suporte a Markdown (Claude Code)
- Prioridade: tudo — progress bars, callouts **e** diagramas

---

## Current Architecture Summary

O OverHarness é um framework YAML/Markdown com 7 agentes e 3 tracks. A formatação visual atual inclui:

**Pontos fortes existentes:**
- Emojis de identidade por agente (🧠🎯🏗️🔧🔬🔎🎨)
- Indicadores de status (✅ ➡️ 🔒 ⬜)
- Tabelas Markdown para metadata
- Hierarquia de headers (H1-H4)
- Code blocks, checklists, Handlebars templating

**Gaps identificados:**
- Sem progress bars visuais
- Sem callouts/admonitions padronizados
- Sem diagramas Mermaid
- Sem separadores de seção ricos
- Bold/italic sem padrão de uso definido
- Sem visual style guide centralizado

---

## Impact Assessment

### Feature 1: Visual Style Guide

| Field | Value |
|-------|-------|
| **Effort** | M |
| **Risk** | Baixo |
| **Priority** | P0 |

**Descrição:** Documento de referência centralizado com todos os padrões visuais do framework — define quando e como usar cada elemento visual com exemplos concretos.

**New Components:**
- `core/style-guide.md` — Guia de estilo visual (~200 linhas)

**Affected Components:**
- Referenciado por todos os agents e instructions (como padrão)

**Risk Details:** Risco baixo — documento novo, não modifica nada existente. Fundamenta todas as outras features.

---

### Feature 2: Callout/Admonition System

| Field | Value |
|-------|-------|
| **Effort** | M |
| **Risk** | Baixo |
| **Priority** | P0 |

**Descrição:** Definir e aplicar padrões de callouts para diferentes tipos de informação: warning, tip, note, success, error, important. Usar blockquotes com emojis como indicadores visuais.

**Affected Components:**
- `core/workflows/**/instructions.md` — Todos os tracks (~20 files)
- `core/workflows/**/template.md` — Todos os templates (~20 files)
- `core/agents/*.agent.yaml` — Seção `style` (~7 files)

**Risk Details:** Risco baixo — mudanças aditivas em arquivos existentes.

---

### Feature 3: Progress Visualization

| Field | Value |
|-------|-------|
| **Effort** | S |
| **Risk** | Baixo |
| **Priority** | P0 |

**Descrição:** Adicionar progress bars ASCII e indicadores de progresso mais ricos à apresentação de status do Sheldon e templates de review.

**Affected Components:**
- `core/agents/sheldon.agent.yaml` — Status e map presentation
- `core/workflows/5-review/template.md` — Summary de review

**Risk Details:** Risco baixo — self-contained, afeta poucos arquivos.

---

### Feature 4: Mermaid Diagrams

| Field | Value |
|-------|-------|
| **Effort** | M |
| **Risk** | Médio |
| **Priority** | P1 |

**Descrição:** Adicionar diagramas Mermaid nos templates de arquitetura e workflow docs — flowcharts, sequence diagrams, class diagrams.

**Affected Components:**
- `core/workflows/3-architecture/template.md` — Component diagrams
- `core/workflows/nf-3-architecture/template.md` — Feature design
- `core/workflows/bf-2-planning/template.md` — Improvement plan
- `core/agents/leonard.agent.yaml` — Style com Mermaid guidance

**Risk Details:** Risco médio — depende de rendering do ambiente. Mitigação: diagramas são supplementary, não substituem texto.

---

### Feature 5: Agent Output Formatting Enhancement

| Field | Value |
|-------|-------|
| **Effort** | M |
| **Risk** | Baixo |
| **Priority** | P0 |

**Descrição:** Enriquecer a seção `persona.style` de cada agente com padrões de formatação específicos — como cada um formata respostas, que elementos visuais usa, como estrutura output.

**Affected Components:**
- `core/agents/sheldon.agent.yaml` — Progress bars, map enhancement
- `core/agents/penny.agent.yaml` — Callouts para requirements
- `core/agents/leonard.agent.yaml` — Mermaid diagrams, trade-off tables
- `core/agents/howard.agent.yaml` — Code blocks, file trees, commit format
- `core/agents/amy.agent.yaml` — Severity indicators, review formatting
- `core/agents/raj.agent.yaml` — Impact matrices, risk callouts
- `core/agents/design-specialist.agent.yaml` — Design tokens, component specs

**Risk Details:** Risco baixo — enriquece a persona sem alterar comportamento.

---

## Summary Matrix

| Feature | Effort | Risk | New Files | Modified Files |
|---------|--------|------|-----------|----------------|
| F1: Visual Style Guide | M | Baixo | 1 | 0 |
| F2: Callout System | M | Baixo | 0 | ~47 |
| F3: Progress Visualization | S | Baixo | 0 | ~3 |
| F4: Mermaid Diagrams | M | Médio | 0 | ~8 |
| F5: Agent Output Enhancement | M | Baixo | 0 | ~7 |

**Total: ~1 arquivo novo, ~50+ arquivos modificados**

---

## Recommendations

1. **Style Guide primeiro** (F1) — fundamenta tudo; define os padrões antes de aplicar
2. **Callouts + Agent Enhancement** (F2+F5) em sequência — aplicação prática do style guide
3. **Progress** (F3) em paralelo — self-contained
4. **Mermaid** (F4) por último — depende de validação de rendering
5. **Implementar em 3 epics:** (1) Foundation (style guide), (2) Application (callouts, agents, progress), (3) Advanced (Mermaid)

---

## Next Steps

- [x] Impact analysis completed
- [ ] Handoff to Penny for feature requirements
- [ ] State.json updated
