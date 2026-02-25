# Improvement Plan: overspec-dev

| Field    | Value                |
|----------|----------------------|
| Project  | overspec-dev         |
| Date     | 2026-02-25           |
| Version  | 1.0                  |
| Agent    | raj                  |
| Phase    | Planning             |

---

## Executive Summary

O OverSpec é um framework bem arquitetado mas com dívida técnica concentrada em schemas desalinhados, workflows incompletos e features não conectadas. Este plano organiza 12 findings do tech debt audit em 4 epics com 14 stories, priorizando **consistência interna primeiro** (schemas) para garantir que toda adição futura seja validável. Abordagem moderada: agrupa quick wins, valida antes de mexer em coisas críticas.

---

## Goals & Objectives

| Goal                                    | Priority | Success Metric                               |
|-----------------------------------------|----------|----------------------------------------------|
| Alinhar schemas com a realidade         | P0       | Todos os 7 agentes e o spec.yaml passam validação contra seus schemas |
| Completar workflows faltantes           | P1       | Flow greenfield e brownfield executáveis end-to-end sem gaps |
| Conectar features configuradas          | P2       | Model profiles e context monitor funcionais   |
| Criar diretórios e paths ausentes       | P0       | Zero referências a caminhos inexistentes      |

---

## Current State Summary

> Extraído do codebase analysis e tech debt report.

- **12 findings** identificados: 1 critical, 4 high, 5 medium, 2 low
- **Schemas** rejeitam os próprios arquivos do framework (agent schema, spec schema)
- **Workflows** com gaps no flow greenfield (requirements) e brownfield (tech-debt-audit)
- **Features** configuradas mas sem efeito (model profiles, context monitor)
- **Diretórios** referenciados mas inexistentes (discuss, discussions, analysis, planning, review)
- **Workflow engine** não documenta actions usadas na prática (auto, party)

---

## Proposed Changes

| ID   | Change                                    | Type     | Priority | Effort | Risk   | Ref    |
|------|-------------------------------------------|----------|----------|--------|--------|--------|
| C-01 | Reescrever agent schema (_schema.json)    | fix      | P0       | M      | Medium | TD-01  |
| C-02 | Corrigir spec schema (workflows structure)| fix      | P0       | S      | Low    | TD-02  |
| C-03 | Corrigir spec.yaml templates paths        | fix      | P0       | S      | Low    | TD-03  |
| C-04 | Criar diretórios faltantes (discuss, discussions, analysis, planning, review) | fix | P0 | XS | Low | TD-10, TD-11 |
| C-05 | Criar workflow requirements (Penny)       | feature  | P1       | M      | Low    | TD-09  |
| C-06 | Criar workflow tech-debt-audit (Raj)      | feature  | P1       | M      | Low    | TD-07  |
| C-07 | Documentar actions auto/party no engine   | fix      | P1       | S      | Low    | TD-12  |
| C-08 | Documentar review compartilhado bf/gf     | fix      | P1       | XS     | Low    | TD-08  |
| C-09 | Integrar model profiles no sistema        | feature  | P2       | M      | Medium | TD-05  |
| C-10 | Implementar context monitor hook          | feature  | P2       | M      | Medium | TD-06  |
| C-11 | Decidir futuro do sistema de tasks        | refactor | P2       | S      | Low    | TD-04  |
| C-12 | Adicionar script de validação de schemas  | feature  | P2       | M      | Low    | —      |

---

## Implementation Roadmap

### Phase 1: Foundation — Consistência Interna
**Timeline:** Imediato (quick wins + schemas)
**Focus:** Garantir que o framework é internamente consistente e validável
**Changes included:** C-01, C-02, C-03, C-04

### Phase 2: Completude — Workflows & Docs
**Timeline:** Após Phase 1
**Focus:** Preencher gaps nos workflows e documentação do engine
**Changes included:** C-05, C-06, C-07, C-08

### Phase 3: Features — Conectar o Desconectado
**Timeline:** Após Phase 2
**Focus:** Ativar features configuradas e limpar indefinições
**Changes included:** C-09, C-10, C-11, C-12

---

## Epics & Stories

### Epic 1: Schema Alignment — Alinhar Schemas com a Realidade

**Goal:** Todos os arquivos de configuração do framework passam validação contra seus schemas.

#### Story 1.1: Reescrever Agent Schema

- **Description:** Reescrever `core/agents/_schema.json` para refletir a estrutura real dos agentes. Suportar fases brownfield (`analysis`, `planning`), o valor especial `all`, campos como `language_protocol`, `behaviors`, `activation` (como array de objetos), e variações por tipo de agente (orchestrator vs. specialist).
- **Effort:** M
- **Priority:** P0
- **Acceptance Criteria:**
  - [ ] Todos os 7 agentes existentes passam validação contra o novo schema
  - [ ] Schema suporta `phases` com valores brownfield e `all`
  - [ ] Schema suporta `activation` como array de objetos com `step` e `detail`
  - [ ] Schema suporta campos opcionais: `language_protocol`, `behaviors`, `first_run_behavior`, `atomic_commits`, `deviation_rules`, `verification_protocol`
  - [ ] Menu items suportam tanto `workflow` quanto `action` como triggers
  - [ ] `additionalProperties` configurado corretamente para não rejeitar campos válidos

#### Story 1.2: Corrigir Spec Schema

- **Description:** Atualizar `schemas/spec-schema.json` para aceitar `components.workflows` como objeto aninhado (com chaves como `greenfield`, `brownfield`) além do formato flat existente.
- **Effort:** S
- **Priority:** P0
- **Acceptance Criteria:**
  - [ ] Schema aceita workflows como array flat OU como objeto com sub-arrays
  - [ ] `specs/software/spec.yaml` passa validação contra o schema corrigido

#### Story 1.3: Corrigir Spec Templates Paths

- **Description:** Atualizar `specs/software/spec.yaml` para que os paths em `components.templates` apontem para os caminhos reais dos templates no disco, ou definir a convenção de resolução de paths no spec-loader.
- **Effort:** S
- **Priority:** P0
- **Acceptance Criteria:**
  - [ ] Paths em `spec.yaml` correspondem aos arquivos reais no disco
  - [ ] Convenção de resolução de paths documentada no spec-loader

#### Story 1.4: Criar Diretórios de Artifacts Faltantes

- **Description:** Criar todos os diretórios de artifacts referenciados por workflows: `artifacts/analysis/`, `artifacts/planning/`, `artifacts/review/`, `artifacts/discuss/`, `artifacts/discussions/`.
- **Effort:** XS
- **Priority:** P0
- **Acceptance Criteria:**
  - [ ] Todos os diretórios referenciados por workflows existem com `.gitkeep`
  - [ ] Zero caminhos de output que apontem para diretórios inexistentes

---

### Epic 2: Workflow Completeness — Preencher Gaps nos Workflows

**Goal:** Flows greenfield e brownfield executáveis end-to-end sem gaps ou referências quebradas.

#### Story 2.1: Criar Workflow Requirements (Penny)

- **Description:** Criar workflow completo para elicitação de requisitos em `1-discovery/`. Penny referencia este workflow no menu mas ele não existe. Leonard e o workflow de arquitetura dependem do artefato `artifacts/discovery/requirements.md` como input obrigatório.
- **Effort:** M
- **Priority:** P1
- **Acceptance Criteria:**
  - [ ] Arquivo `requirements-workflow.yaml` criado em `core/workflows/1-discovery/`
  - [ ] Template `requirements-template.md` criado
  - [ ] Checklist `requirements-checklist.md` criado
  - [ ] Instructions `requirements-instructions.md` criado
  - [ ] Workflow produz `artifacts/discovery/requirements.md`
  - [ ] Output tem `handoff_to: [leonard]`

#### Story 2.2: Criar Workflow Tech-Debt-Audit (Raj)

- **Description:** Criar workflow dedicado para auditoria de dívida técnica no flow brownfield. Atualmente Raj tem behavior para isso mas sem workflow formal com template e checklist.
- **Effort:** M
- **Priority:** P1
- **Acceptance Criteria:**
  - [ ] Workflow YAML criado (pode ser no mesmo diretório `bf-1-analysis/` ou em subdiretório)
  - [ ] Template para tech-debt-report criado
  - [ ] Checklist para validação criado
  - [ ] Instructions com procedimento de auditoria criado
  - [ ] Workflow produz `artifacts/analysis/tech-debt-report.md`

#### Story 2.3: Documentar Actions Não-Padrão no Workflow Engine

- **Description:** Adicionar documentação para as actions `auto` e `party` no `workflow-engine.md`, que são usadas pelo party-mode mas não estão documentadas no engine.
- **Effort:** S
- **Priority:** P1
- **Acceptance Criteria:**
  - [ ] Actions `auto` e `party` documentadas no workflow-engine.md com instruções de processamento
  - [ ] Exemplos de uso incluídos

#### Story 2.4: Documentar Review Compartilhado

- **Description:** Adicionar nota explicativa no workflow `5-review/` e/ou na spec.yaml que a fase de review é compartilhada entre greenfield e brownfield, justificando por que não existe `bf-4-review/`.
- **Effort:** XS
- **Priority:** P1
- **Acceptance Criteria:**
  - [ ] Documentação clara sobre o compartilhamento em pelo menos um dos arquivos relevantes

---

### Epic 3: Feature Activation — Conectar Features Desconectadas

**Goal:** Features configuradas no framework passam a ter efeito real no comportamento dos agentes.

#### Story 3.1: Integrar Model Profiles

- **Description:** Conectar `model_profiles` do `overspec.yaml` ao sistema de agentes. Quando Sheldon delega para um agente, a ativação deveria indicar qual modelo usar baseado no perfil ativo (`quality`, `balanced`, `budget`).
- **Effort:** M
- **Priority:** P2
- **Acceptance Criteria:**
  - [ ] Sheldon lê o perfil ativo ao delegar para agentes
  - [ ] A ativação dos agentes inclui indicação do modelo recomendado
  - [ ] Documentação de como os perfis afetam o comportamento

#### Story 3.2: Implementar Context Monitor

- **Description:** Transformar o context-monitor.md de documentação pura em funcionalidade real. Implementar como instruções nos agentes para auto-monitorar o uso de contexto e criar checkpoints proativamente.
- **Effort:** M
- **Priority:** P2
- **Acceptance Criteria:**
  - [ ] Agentes incluem instruções de auto-monitoramento de contexto
  - [ ] Integração com o sistema de checkpoints do workflow engine
  - [ ] Pelo menos 2 agentes (os que rodam workflows longos) têm a instrução

#### Story 3.3: Decidir Futuro do Sistema de Tasks

- **Description:** O `core/tasks/` está vazio e o spec schema suporta tasks, mas nada existe. Decidir: implementar como unidades granulares dentro de workflows, ou remover do schema.
- **Effort:** S
- **Priority:** P2
- **Acceptance Criteria:**
  - [ ] Decisão documentada (implementar ou remover)
  - [ ] Se remover: limpar referências do schema e da estrutura
  - [ ] Se implementar: criar pelo menos 1 task de exemplo e documentar a diferença entre tasks e steps

#### Story 3.4: Criar Script de Validação

- **Description:** Criar um script simples (shell) que valida todos os YAML/JSON files contra seus schemas, para detectar inconsistências automaticamente.
- **Effort:** M
- **Priority:** P2
- **Acceptance Criteria:**
  - [ ] Script valida agents contra _schema.json
  - [ ] Script valida spec.yaml contra spec-schema.json
  - [ ] Script valida team files contra team-schema.json
  - [ ] Script reporta erros claramente com file paths

---

## Risk Assessment

| Risk                                    | Probabilidade | Impacto | Mitigação                                  |
|-----------------------------------------|---------------|---------|---------------------------------------------|
| Mudança no agent schema quebra Bernadette (gera specs com schema antigo) | Média | Alto | Atualizar Bernadette's spec-designer-guide junto com o schema |
| Novo workflow requirements não se encaixa no flow existente de Penny | Baixa | Médio | Seguir o padrão dos workflows existentes (1-discovery/project-brief como referência) |
| Model profiles adicionam complexidade sem valor claro | Baixa | Baixo | Implementar de forma opt-in — se o perfil não está configurado, comportamento padrão |
| Muitas mudanças simultâneas criam inconsistências | Média | Alto | Seguir o roadmap em fases — validar Phase 1 antes de iniciar Phase 2 |

---

## Dependencies & Constraints

**Dependencies:**

- C-01 (agent schema) deve ser feito antes de C-12 (script de validação)
- C-02 (spec schema) deve ser feito antes de C-12 (script de validação)
- C-04 (diretórios) deve ser feito antes de C-05 e C-06 (novos workflows que geram artefatos)
- C-05 (workflow requirements) é pré-requisito para o flow greenfield funcionar end-to-end
- Phase 1 completa antes de Phase 2; Phase 2 completa antes de Phase 3

**Constraints:**

- Sem restrições declaradas pelo usuário — tudo pode ser modificado
- Abordagem moderada: agrupar quick wins, validar antes de mexer em coisas críticas
- Manter retrocompatibilidade da spec software com o flow atual

---

## Success Metrics

- **Schema Compliance:** 100% dos arquivos de configuração passam validação contra seus schemas (Target: 100%)
- **Workflow Coverage:** Zero gaps em flows greenfield e brownfield — todos os steps no state.json têm workflow correspondente (Target: 0 gaps)
- **Feature Activation:** Model profiles e context monitor funcionais e documentados (Target: 2/2 features ativas)
- **Path Integrity:** Zero referências a caminhos inexistentes em workflows (Target: 0 broken paths)

---

## Next Steps

> Section automatically filled by the system.

- [ ] Plan reviewed and approved by the user
- [ ] Handoff created for the next agent (howard)
- [ ] State.json updated with status `completed`
