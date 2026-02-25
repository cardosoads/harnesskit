# Brownfield Setup Report: overspec-dev

| Field    | Value                       |
|----------|-----------------------------|
| Project  | overspec-dev                |
| Date     | 2026-02-25                  |
| Version  | 1.0                         |
| Agent    | howard                      |
| Phase    | Implementation (Brownfield) |

---

## Improvement Plan Summary

**Total Epics:** 4
**Total Stories:** 14
**Top Priority:** P0 — Schema Alignment (Epic 1)
**Risk Tolerance:** Moderado

---

## Selected Epic / Story

**Epic:** Epic 1 — Schema Alignment
**Story:** Story 1.1 — Reescrever Agent Schema
**Priority:** P0
**Effort:** M
**Risk:** Medium

**Acceptance Criteria:**

- [ ] Todos os 7 agentes existentes passam validação contra o novo schema
- [ ] Schema suporta `phases` com valores brownfield e `all`
- [ ] Schema suporta `activation` como array de objetos com `step` e `detail`
- [ ] Schema suporta campos opcionais: `language_protocol`, `behaviors`, `first_run_behavior`, `atomic_commits`, `deviation_rules`, `verification_protocol`
- [ ] Menu items suportam tanto `workflow` quanto `action` como triggers
- [ ] `additionalProperties` configurado corretamente para não rejeitar campos válidos

---

## Current State

O agent schema atual (`core/agents/_schema.json`) é um JSON Schema draft-07 que não aceita os próprios agentes do framework. Principais incompatibilidades:

- `phases` enum não inclui brownfield values ou `all`
- `activation` espera strings, agentes usam objetos
- `menu` exige `workflow`, Sheldon usa `action`
- `additionalProperties: false` rejeita campos essenciais

**Affected Files:**

- `core/agents/_schema.json` — Schema a ser reescrito

**Affected Components:**

- **Agent Definitions** (Healthy) — Não serão alterados, apenas o schema
- **Spec Designer Guide** (Healthy) — Bernadette usa o schema como referência; atualizar se necessário
- **Schemas** (Needs Attention) — Impacto direto

---

## Proposed Changes

| File / Area              | What Changes                     | Why                                    |
|--------------------------|----------------------------------|----------------------------------------|
| `core/agents/_schema.json` | Reescrever completamente      | Schema atual rejeita todos os 7 agentes |

---

## Safety Net

**Test Coverage (before):** 0% automatizado — validação manual via revisão

**Backup Strategy:** Branch separada (`feature/schema-alignment`)

**Rollback Plan:** `git revert` do commit específico; branch pode ser deletada sem afetar main

**Pre-change Verification:**

- [x] Todos os agentes atuais lidos e analisados (durante codebase analysis)
- [ ] Feature branch criada
- [x] Backup/snapshot via git (main branch intacta)

---

## Implementation Steps

### Step 1: Criar Feature Branch

**Action:** Criar branch `feature/schema-alignment` a partir de main

**Verification:** `git branch` confirma branch criada

**Rollback:** `git checkout main && git branch -D feature/schema-alignment`

### Step 2: Reescrever Agent Schema

**Action:** Reescrever `core/agents/_schema.json` com schema compatível com todos os 7 agentes. Incluir suporte a: phases brownfield + all, activation como objetos, menu com workflow ou action, campos opcionais por tipo de agente.

**Verification:** Validar mentalmente cada um dos 7 agentes contra o novo schema

**Rollback:** `git checkout -- core/agents/_schema.json`

### Step 3: Commit Atômico

**Action:** `fix(03-01): rewrite agent schema to match actual agent definitions`

**Verification:** `git log --oneline -1` confirma commit

**Rollback:** `git revert HEAD`

---

## Verification Plan

**After implementation, verify:**

- [ ] sheldon.agent.yaml passa validação (orchestrator com `phases: [all]`, menu com `action`)
- [ ] penny.agent.yaml passa validação (specialist com `phases: [discovery, specification]`)
- [ ] leonard.agent.yaml passa validação (specialist com `phases: [architecture]`)
- [ ] howard.agent.yaml passa validação (specialist com `atomic_commits`, `deviation_rules`)
- [ ] amy.agent.yaml passa validação (specialist com `verification_protocol`)
- [ ] raj.agent.yaml passa validação (brownfield com `phases: [analysis, planning]`)
- [ ] bernadette.agent.yaml passa validação (designer com `phases: [all]`)

---

## Next Steps

- [x] Setup report reviewed and approved by the user
- [ ] Implementation executed
- [ ] Handoff created for the next agent (amy)
- [ ] State.json updated with status `completed`
