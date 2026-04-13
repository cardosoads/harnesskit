# Improvement Plan: harnesskit-dev (Ciclo 2)

| Field    | Value                         |
|----------|-------------------------------|
| Project  | harnesskit-dev                  |
| Date     | 2026-02-25                    |
| Version  | 2.0                           |
| Agent    | raj                           |
| Phase    | Planning (Cycle 2)            |

---

## Executive Summary

Adicionar o track **New Features** ao Harnesskit — um terceiro fluxo de trabalho para adicionar features a projetos existentes. O track combina Raj (análise de impacto no codebase) + Penny (requisitos da feature) na discovery, seguido por especificação, arquitetura, implementação e review. O plano organiza o trabalho em 3 epics com 10 stories.

---

## Goals & Objectives

| Goal                                           | Priority | Success Metric                                    |
|------------------------------------------------|----------|---------------------------------------------------|
| Track new-features funcional end-to-end        | P0       | Sheldon reconhece, roteia e executa o novo track   |
| Discovery com Raj + Penny integrada            | P0       | Handoff intra-fase funciona (raj → penny)          |
| State machine dinâmica                         | P1       | Suporta qualquer número de tracks sem hardcode     |
| Workflows completos com 4 arquivos cada        | P0       | Todos os workflows têm yaml + instructions + template + checklist |

---

## Epics & Stories

### Epic 1: Infraestrutura do Track — Configuração e Roteamento

**Goal:** O framework reconhece "new-features" como um terceiro project_type e Sheldon consegue rotear o usuário pelo novo fluxo.

#### Story 1.1: Adicionar newfeatures_phases no harnesskit.yaml

- **Description:** Adicionar a seção `newfeatures_phases` com as 5 fases: discovery, specification, architecture, implementation, review.
- **Effort:** XS
- **Acceptance Criteria:**
  - [ ] Seção `newfeatures_phases` existe em `harnesskit.yaml`
  - [ ] 5 fases definidas com `enabled: true` e `order` correto

#### Story 1.2: Atualizar Sheldon para suportar 3 tracks

- **Description:** Atualizar `sheldon.agent.yaml` para: (1) apresentar 3 opções no `project_type_detection`, (2) adicionar phase map para new-features, (3) atualizar `new_project_detection` com texto para o novo track, (4) explicar que Raj + Penny trabalham juntos na discovery.
- **Effort:** M
- **Acceptance Criteria:**
  - [ ] `project_type_detection` apresenta 3 opções (greenfield, brownfield, new-features)
  - [ ] Phase map inclui visualização do novo track
  - [ ] `new_project_detection` tem texto específico para new-features
  - [ ] Sheldon sabe que discovery usa Raj + Penny

#### Story 1.3: Tornar state-machine.md dinâmico

- **Description:** Substituir a lista hardcoded de fases (linha 77-81) por instrução genérica que lê as fases do `harnesskit.yaml` baseado no `project_type`.
- **Effort:** S
- **Acceptance Criteria:**
  - [ ] Nenhuma lista hardcoded de fases no state-machine.md
  - [ ] Instrução genérica referencia `harnesskit.yaml > {project_type}_phases`

#### Story 1.4: Criar team-newfeatures.yaml

- **Description:** Criar preset de team para o track new-features com os agentes: penny, raj, leonard, howard, amy.
- **Effort:** XS
- **Acceptance Criteria:**
  - [ ] Arquivo `teams/team-newfeatures.yaml` existe
  - [ ] Inclui os 5 agentes necessários

#### Story 1.5: Registrar track no spec.yaml

- **Description:** Adicionar seção `newfeatures` em `components.workflows` e `components.templates` no `specs/software/spec.yaml`.
- **Effort:** XS
- **Acceptance Criteria:**
  - [ ] Workflows do track listados em spec.yaml
  - [ ] Templates do track listados em spec.yaml

---

### Epic 2: Workflows — Discovery, Specification, Architecture, Implementation

**Goal:** Todos os workflows do track new-features estão completos com os 4 arquivos padrão (yaml + instructions + template + checklist).

#### Story 2.1: Criar workflow nf-1-discovery (Raj: impact analysis)

- **Description:** Criar o primeiro sub-workflow da discovery: Raj analisa o codebase existente e avalia o impacto da feature proposta. Produz um relatório de análise de impacto.
- **Effort:** M
- **Acceptance Criteria:**
  - [ ] `nf-1-discovery/impact-analysis-workflow.yaml` criado
  - [ ] `nf-1-discovery/impact-analysis-instructions.md` criado
  - [ ] `nf-1-discovery/impact-analysis-template.md` criado
  - [ ] `nf-1-discovery/impact-analysis-checklist.md` criado
  - [ ] Output: `artifacts/discovery/impact-analysis.md`
  - [ ] Handoff: raj → penny

#### Story 2.2: Criar workflow nf-1-discovery (Penny: feature requirements)

- **Description:** Criar o segundo sub-workflow da discovery: Penny recebe a análise de impacto do Raj e levanta os requisitos da feature com o usuário via brainstorm. Produz um documento de requisitos da feature.
- **Effort:** M
- **Acceptance Criteria:**
  - [ ] `nf-1-discovery/feature-requirements-workflow.yaml` criado
  - [ ] `nf-1-discovery/feature-requirements-instructions.md` criado
  - [ ] `nf-1-discovery/feature-requirements-template.md` criado
  - [ ] `nf-1-discovery/feature-requirements-checklist.md` criado
  - [ ] Input: `artifacts/discovery/impact-analysis.md`
  - [ ] Output: `artifacts/discovery/feature-requirements.md`
  - [ ] Handoff: penny → penny (specification)

#### Story 2.3: Criar workflow nf-2-specification

- **Description:** Criar o workflow de especificação: Penny detalha os requisitos em user stories com acceptance criteria. Adaptado para features em projeto existente (referencia arquitetura e codebase existentes).
- **Effort:** M
- **Acceptance Criteria:**
  - [ ] 4 arquivos padrão criados em `nf-2-specification/`
  - [ ] Input: `artifacts/discovery/feature-requirements.md`
  - [ ] Output: `artifacts/specification/feature-stories.md`
  - [ ] Handoff: penny → leonard

#### Story 2.4: Criar workflow nf-3-architecture

- **Description:** Criar o workflow de arquitetura: Leonard analisa como a feature se encaixa na arquitetura existente. Foco em integração, não em criação do zero. Produz um design document.
- **Effort:** M
- **Acceptance Criteria:**
  - [ ] 4 arquivos padrão criados em `nf-3-architecture/`
  - [ ] Input: `artifacts/specification/feature-stories.md`
  - [ ] Output: `artifacts/architecture/feature-design.md`
  - [ ] Handoff: leonard → howard

#### Story 2.5: Criar workflow nf-4-implementation

- **Description:** Criar o workflow de implementação: Howard implementa as stories seguindo o design. Similar ao bf-3-implementation mas orientado por feature stories em vez de improvement plan.
- **Effort:** M
- **Acceptance Criteria:**
  - [ ] 4 arquivos padrão criados em `nf-4-implementation/`
  - [ ] Input: `artifacts/architecture/feature-design.md`
  - [ ] Output: `artifacts/implementation/feature-report.md`
  - [ ] Handoff: howard → amy

---

### Epic 3: Integração e Polimento

**Goal:** O track funciona end-to-end e está documentado.

#### Story 3.1: Criar diretórios de artifacts para new-features

- **Description:** Garantir que todos os diretórios de artifacts referenciados pelos workflows existam.
- **Effort:** XS
- **Acceptance Criteria:**
  - [ ] Todos os paths de output dos workflows apontam para diretórios existentes

#### Story 3.2: Atualizar 5-review/workflow.yaml para mencionar 3 tracks

- **Description:** Atualizar o comentário do review para mencionar que é compartilhado entre greenfield, brownfield e new-features.
- **Effort:** XS
- **Acceptance Criteria:**
  - [ ] Comentário menciona os 3 tracks

---

## Implementation Roadmap

### Phase 1: Infraestrutura (Epic 1)
**Stories:** 1.1, 1.2, 1.3, 1.4, 1.5
**Focus:** O framework reconhece o novo track

### Phase 2: Workflows (Epic 2)
**Stories:** 2.1, 2.2, 2.3, 2.4, 2.5
**Focus:** Workflows completos para cada fase

### Phase 3: Integração (Epic 3)
**Stories:** 3.1, 3.2
**Focus:** Polimento e consistência

---

## Dependencies

- Story 1.1 deve ser feita antes de 1.2 (Sheldon precisa conhecer as fases)
- Story 2.1 deve ser feita antes de 2.2 (Penny depende do output do Raj)
- Epic 1 deve estar completo antes do Epic 2 (infraestrutura antes de workflows)
- Epic 2 deve estar completo antes do Epic 3 (workflows antes de integração)

---

## Risk Assessment

| Risk | Probabilidade | Impacto | Mitigação |
|------|---------------|---------|-----------|
| Discovery com 2 agentes é padrão novo — pode confundir | Média | Médio | Documentar claramente o handoff intra-fase no workflow |
| Muitos arquivos novos (~20) | Baixa | Baixo | Seguir padrão dos workflows existentes |
| State machine hardcoded quebra com novo track | Alta | Alto | Story 1.3 resolve antes de qualquer coisa |

---

## Success Metrics

- **Track funcional:** Sheldon consegue iniciar e rotear um projeto new-features end-to-end
- **Workflow coverage:** 5 fases com workflows completos (4 novos + 1 reutilizado)
- **Validation:** Script de validação continua passando 100%
- **Consistência:** Todos os workflows seguem o padrão de 4 arquivos

---

## Next Steps

- [ ] Plan reviewed and approved by the user
- [ ] Handoff created for howard
- [ ] State.json updated with status `completed`
