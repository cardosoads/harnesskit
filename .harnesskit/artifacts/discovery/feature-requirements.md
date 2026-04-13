# Feature Requirements: Visual CLI Enhancement

| Field    | Value                      |
|----------|----------------------------|
| Project  | harnesskit-dev               |
| Date     | 2026-02-25                 |
| Version  | 4.0                        |
| Agent    | penny                      |
| Phase    | Discovery (New Features)   |
| Cycle    | 4                          |
| Based on | Impact Analysis by raj     |

---

## Executive Summary

Melhoria visual completa do framework Harnesskit para ambiente CLI com Markdown rendering (Claude Code). O framework atual tem formatação básica mas funcional. O objetivo é elevar a experiência visual com: (1) um **Visual Style Guide** centralizado que define todos os padrões, (2) um sistema de **callouts/admonitions** para informações contextuais, (3) **progress bars** e indicadores visuais mais ricos, (4) **diagramas Mermaid** para visualização de workflows e arquitetura, e (5) **formatação enriquecida nos agentes** com padrões de output específicos por persona.

**Contexto técnico:** O Harnesskit é puramente YAML/Markdown — não tem runtime code. Toda formatação visual é definida em agent.yaml (seção `persona.style`), instructions.md (guia de como o agente formata) e template.md (estrutura dos artefatos). O ambiente de rendering é Claude Code (terminal com suporte a Markdown, incluindo code blocks, tabelas, Mermaid, e blockquotes).

---

## Features

### F1 — Visual Style Guide

**Description:** Criar um documento de referência centralizado (`core/style-guide.md`) que define todos os padrões visuais do framework — quando usar cada elemento, com exemplos concretos e anti-patterns.

**User/Persona:** Todos os agentes (consultam o style guide) e futuros autores de specs/agents.

**Impact Summary (from Raj):** 1 arquivo novo. Risco baixo. Fundamenta todas as outras features.

#### Functional Requirements

- **FR-1.1:** O style guide deve definir **6 tipos de callouts** com emoji + formato:
  - `> ⚠️ **Warning:**` — Riscos, breaking changes, ações irreversíveis
  - `> 💡 **Tip:**` — Sugestões, boas práticas, atalhos
  - `> 📌 **Note:**` — Informação contextual, esclarecimentos
  - `> ✅ **Success:**` — Confirmações, resultados positivos
  - `> ❌ **Error:**` — Falhas, erros, problemas encontrados
  - `> 📋 **Important:**` — Informação crítica que não pode ser ignorada
- **FR-1.2:** O style guide deve definir **progress bar format**:
  - Formato: `████████░░ 80% (4/5 phases)`
  - Caracteres: `█` (preenchido) e `░` (vazio)
  - Sempre incluir percentual e contagem
- **FR-1.3:** O style guide deve definir **padrões de Mermaid** para:
  - Flowchart (workflow visualization)
  - Sequence diagram (handoff chains)
  - Class/ER diagrams (architecture components)
- **FR-1.4:** O style guide deve definir **padrões de emphasis**:
  - **Bold** — Termos-chave, nomes de agentes, nomes de fases, labels
  - *Italic* — Termos técnicos na primeira menção, citações, ênfase suave
  - `Code` — Paths, filenames, variáveis, comandos, IDs
  - ~~Strikethrough~~ — Itens removidos, deprecated
- **FR-1.5:** O style guide deve definir **separadores de seção**:
  - `---` entre seções principais (como hoje)
  - Uso consistente de H2 para seções, H3 para subseções, H4 para items
- **FR-1.6:** O style guide deve incluir **anti-patterns** — o que NÃO fazer (formatação excessiva, emojis em excesso, tabelas onde listas bastam)
- **FR-1.7:** O style guide deve ser referenciado no `persona.style` de cada agente como padrão base

#### Non-Functional Requirements

- **NFR-1.1:** O style guide deve ter no máximo ~200 linhas — conciso, não um manual
- **NFR-1.2:** Exemplos devem ser copy-pasteable — agentes podem usar como referência direta

#### Acceptance Criteria

- **AC-1.1:** Given o style guide existe, When lido, Then cobre callouts, progress bars, Mermaid, emphasis e anti-patterns
- **AC-1.2:** Given um agente consulta o style guide, When formata output, Then consegue encontrar o padrão correto em <30 segundos de leitura
- **AC-1.3:** Given o style guide define um callout, When um agente usa, Then o formato visual é consistente em todos os agentes

---

### F2 — Callout/Admonition System

**Description:** Aplicar o sistema de callouts definido no style guide a todos os instructions.md e template.md existentes. Adicionar callouts contextuais onde informação importante, warnings ou tips existem em formato plain text.

**User/Persona:** Todos os agentes (seguem as instructions) e o usuário (lê os artefatos).

**Impact Summary (from Raj):** 0 arquivos novos, ~40 arquivos modificados (instructions + templates). Risco baixo.

#### Functional Requirements

- **FR-2.1:** Todos os `instructions.md` devem usar callouts nos seguintes contextos:
  - `> 📋 **Important:**` — Regras que o agente DEVE seguir (ex: language protocol, constitution principles)
  - `> ⚠️ **Warning:**` — Ações que podem causar problemas se ignoradas (ex: não pular fases)
  - `> 💡 **Tip:**` — Sugestões para melhor resultado (ex: "pergunte ao usuário se X está claro")
- **FR-2.2:** Todos os `template.md` devem usar callouts nos seguintes contextos:
  - `> 📌 **Note:**` — Informação contextual sobre a seção (ex: "preenchido automaticamente pelo sistema")
  - `> 💡 **Tip:**` — Orientação para quem preenche o template
- **FR-2.3:** Callouts existentes em formato plain text (ex: `> IMPORTANT: ...`) devem ser migrados para o novo formato padronizado
- **FR-2.4:** Callouts devem ser usados com moderação — máximo 3-4 por arquivo, posicionados em pontos críticos

#### Non-Functional Requirements

- **NFR-2.1:** Mudanças são aditivas — o conteúdo existente não é alterado, apenas formatado
- **NFR-2.2:** Callouts devem render corretamente como blockquotes em Markdown padrão

#### Acceptance Criteria

- **AC-2.1:** Given um instructions.md é lido, When contém regras críticas, Then usa callout `> 📋 **Important:**`
- **AC-2.2:** Given todos os instructions.md são inspecionados, When callouts são contados, Then nenhum arquivo tem mais de 5 callouts
- **AC-2.3:** Given callouts antigos existiam (formato `> IMPORTANT:`), When migrados, Then usam o novo formato padronizado

---

### F3 — Progress Visualization

**Description:** Adicionar progress bars visuais ASCII e indicadores de progresso enriquecidos à apresentação de status do Sheldon e aos templates de review.

**User/Persona:** Sheldon (apresentação de status) e Amy (review report).

**Impact Summary (from Raj):** 0 arquivos novos, ~3 arquivos modificados. Risco baixo.

#### Functional Requirements

- **FR-3.1:** Sheldon deve mostrar **progress bar** no status do projeto:
  ```
  Progress: ████████░░ 80% (4/5 phases)
  ```
- **FR-3.2:** Sheldon deve mostrar **progress bar por fase** no status detalhado:
  ```
  Specification: ██████░░░░ 60% (3/5 steps)
  ```
- **FR-3.3:** Amy deve incluir progress bar no review report para indicar compliance:
  ```
  Compliance: ██████████ 100% (14/14 items passed)
  ```
- **FR-3.4:** O formato de progress bar deve ser definido na seção `activation` do Sheldon (visual status presentation)
- **FR-3.5:** Progress bars devem ter **largura fixa** de 10 caracteres (`██████████`) para alinhamento visual

#### Non-Functional Requirements

- **NFR-3.1:** Progress bars devem usar Unicode block characters (`█` e `░`) — suportados em todos os terminais modernos
- **NFR-3.2:** Self-contained — não depende de outras features

#### Acceptance Criteria

- **AC-3.1:** Given Sheldon mostra status, When o projeto está 60% completo, Then mostra `██████░░░░ 60%`
- **AC-3.2:** Given Amy completa review, When gera report, Then inclui compliance bar
- **AC-3.3:** Given progress bar é renderizada, When vista no terminal, Then tem largura consistente de 10 chars

---

### F4 — Mermaid Diagrams

**Description:** Adicionar suporte a diagramas Mermaid nos templates de arquitetura, workflow visualizations e engine docs. Diagramas são supplementary (não substituem texto).

**User/Persona:** Leonard (architecture), Sheldon (workflow visualization), documentação do engine.

**Impact Summary (from Raj):** 0 arquivos novos, ~8 arquivos modificados. Risco médio.

#### Functional Requirements

- **FR-4.1:** Template de **architecture** (greenfield + brownfield + new-features) deve incluir seção de Mermaid para:
  - Component diagram (flowchart mostrando componentes e suas conexões)
  - Data flow diagram (sequence diagram mostrando fluxo de dados)
- **FR-4.2:** Template de **architecture** deve ter instruções de como popular o Mermaid diagram com placeholders Handlebars
- **FR-4.3:** Instructions do **Leonard** devem mencionar que diagramas Mermaid são esperados no output de arquitetura
- **FR-4.4:** O **style guide** deve incluir exemplos de Mermaid para os 3 tipos (flowchart, sequence, class/ER)
- **FR-4.5:** Diagramas Mermaid devem sempre ter um **fallback texto** — uma descrição em prosa antes ou depois do diagrama
- **FR-4.6:** Sheldon pode usar Mermaid para visualizar o **workflow pipeline** (discovery → specification → architecture → implementation → review)

#### Non-Functional Requirements

- **NFR-4.1:** Mermaid é supplementary — se não renderiza, o texto alternativo cobre a informação
- **NFR-4.2:** Diagramas devem ser simples — máximo 10-15 nós para manter legibilidade

#### Acceptance Criteria

- **AC-4.1:** Given o template de architecture é usado, When Leonard gera o artifact, Then inclui pelo menos 1 diagrama Mermaid
- **AC-4.2:** Given um diagrama Mermaid está no output, When o terminal não suporta Mermaid, Then existe texto descritivo como fallback
- **AC-4.3:** Given o style guide é consultado, When Mermaid é procurado, Then encontra exemplos dos 3 tipos

---

### F5 — Agent Output Formatting Enhancement

**Description:** Enriquecer a seção `persona.style` de cada agente com padrões de formatação específicos — como cada agente formata suas respostas, quais elementos visuais usa, e como estrutura output. Referencia o style guide como base.

**User/Persona:** Cada agente individualmente.

**Impact Summary (from Raj):** 0 arquivos novos, ~7 agent.yaml modificados. Risco baixo.

#### Functional Requirements

- **FR-5.1:** Cada agente deve ter na seção `persona.style` uma referência ao style guide: "Follows formatting patterns from `core/style-guide.md`"
- **FR-5.2:** **Sheldon** deve ter formatting directives adicionais:
  - Progress bars no status e map
  - Mermaid flowchart opcional para workflow pipeline
  - Callouts `📋 Important` para principles do Constitution
- **FR-5.3:** **Penny** deve ter formatting directives:
  - Callouts `💡 Tip` para orientar o usuário nas respostas
  - Tabelas de summary em feature requirements
  - Listas numeradas para requirements (FRs)
- **FR-5.4:** **Leonard** deve ter formatting directives:
  - Mermaid diagrams para componentes e data flow
  - Trade-off tables com pros/cons
  - Callouts `⚠️ Warning` para riscos arquiteturais
- **FR-5.5:** **Howard** deve ter formatting directives:
  - Code blocks com syntax highlighting (language specifier)
  - File trees com Unicode box-drawing
  - Callouts `📋 Important` para regras de implementação
- **FR-5.6:** **Amy** deve ter formatting directives:
  - Progress/compliance bars no review report
  - Severity indicators com emoji (🔴 Critical, 🟡 Warning, 🟢 Info)
  - Callouts `❌ Error` para issues encontradas
- **FR-5.7:** **Raj** deve ter formatting directives:
  - Impact matrices com tabelas
  - Risk callouts `⚠️ Warning` para áreas de alto impacto
  - Callouts `📌 Note` para observações do codebase
- **FR-5.8:** **Emily** deve ter formatting directives:
  - Design token examples em code blocks
  - Component state tables
  - Callouts `💡 Tip` para orientação de art direction

#### Non-Functional Requirements

- **NFR-5.1:** Formatting directives são adições à `persona.style` — não substituem a personalidade existente
- **NFR-5.2:** Cada agente mantém sua voz — o style guide é a base, a personalidade é o diferencial

#### Acceptance Criteria

- **AC-5.1:** Given cada agent.yaml é lido, When `persona.style` é inspecionado, Then referencia o style guide
- **AC-5.2:** Given Sheldon apresenta status, When formatado, Then inclui progress bars
- **AC-5.3:** Given Amy gera review, When issues são encontradas, Then usa severity indicators com emoji
- **AC-5.4:** Given Leonard gera architecture, When componentes são descritos, Then inclui Mermaid diagram

---

## Summary Matrix

| Feature | Priority | Effort | Risk | FRs | ACs |
|---------|----------|--------|------|-----|-----|
| F1 — Visual Style Guide | P0 | M | Baixo | 7 | 3 |
| F2 — Callout System | P0 | M | Baixo | 4 | 3 |
| F3 — Progress Visualization | P0 | S | Baixo | 5 | 3 |
| F4 — Mermaid Diagrams | P1 | M | Médio | 6 | 3 |
| F5 — Agent Output Enhancement | P0 | M | Baixo | 8 | 4 |

**Total: 30 functional requirements, 16 acceptance criteria**

---

## Scope Decisions

### In Scope

- Visual Style Guide com padrões de callouts, progress, Mermaid, emphasis
- Aplicação de callouts a todos os instructions.md e templates.md
- Progress bars no Sheldon (status) e Amy (review)
- Mermaid diagrams nos templates de architecture
- Enrichment da seção `persona.style` de cada agente
- Anti-patterns (o que não fazer)

### Out of Scope

- ANSI color codes (não portável entre terminais)
- Animações/interatividade (CLI é estático)
- Mudanças no Handlebars templating engine (só formatação)
- Redesign de estrutura de seções (só enriquecimento visual)
- Mudanças em checklists (formato checkbox funciona bem)

---

## Next Steps

- [x] Feature requirements completed
- [ ] Handoff to specification phase (penny)
- [ ] State.json updated
