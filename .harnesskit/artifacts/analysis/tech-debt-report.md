# Tech Debt Report: harnesskit-dev

| Field    | Value                |
|----------|----------------------|
| Project  | harnesskit-dev         |
| Date     | 2026-02-25           |
| Version  | 1.0                  |
| Agent    | raj                  |
| Phase    | Analysis             |

---

## Executive Summary

O Harnesskit é um framework jovem e bem arquitetado, mas com dívida técnica concentrada em **3 áreas principais**: (1) schemas desalinhados que impedem validação real, (2) features configuradas mas não conectadas ao sistema, e (3) gaps na cobertura de workflows brownfield. A dívida é estrutural, não de código — o que a torna mais fácil de corrigir incrementalmente.

**Findings totais:** 12
- Critical: 1
- High: 4
- Medium: 5
- Low: 2

---

## Findings

### TD-01 — Agent Schema Não Reflete a Realidade

| Field | Value |
|-------|-------|
| **Severidade** | Critical |
| **Esforço** | M |
| **Impacto** | Validação de agentes é impossível; novos agentes criados por Bernadette não podem ser validados |
| **Ação** | Fix Now |

**Descrição:** O `_schema.json` dos agentes tem múltiplas incompatibilidades com os arquivos reais:

1. `phases` é definido como enum `["discovery", "specification", "architecture", "implementation", "review"]` — mas agentes brownfield usam `"analysis"` e `"planning"`, e Sheldon/Bernadette usam `[all]`
2. `activation` é definido como `array of strings` — mas nos agentes reais é `array of objects` com campos `step` e `detail`
3. `additionalProperties: false` rejeita campos essenciais que existem em todos os agentes: `language_protocol`, `behaviors`, `first_run_behavior` (Sheldon), `atomic_commits` e `deviation_rules` (Howard), `verification_protocol` (Amy)
4. `menu` exige `workflow` como campo obrigatório — mas o menu de Sheldon usa `action` em vez de `workflow`

**Evidência:** Comparação direta entre `core/agents/_schema.json` e todos os 7 arquivos `.agent.yaml`.

**Recomendação:** Reescrever o `_schema.json` para refletir a estrutura real dos agentes. Considerar usar `oneOf` para diferenciar schemas de agentes orquestradores (Sheldon) vs. agentes especialistas.

---

### TD-02 — Spec Schema `workflows` Incompatível

| Field | Value |
|-------|-------|
| **Severidade** | High |
| **Esforço** | S |
| **Impacto** | A spec `software` não passa validação contra seu próprio schema |
| **Ação** | Fix Now |

**Descrição:** O `spec-schema.json` define `components.workflows` como um `array` de strings. Porém, o `spec.yaml` real usa um objeto aninhado com chaves `greenfield` e `brownfield`, cada uma contendo um array de strings.

**Evidência:**
- Schema (`schemas/spec-schema.json`, linha 76-82): `"workflows": { "type": "array", "items": { "type": "string" } }`
- Realidade (`specs/software/spec.yaml`, linha 30-42): `workflows: { greenfield: [...], brownfield: [...] }`

**Recomendação:** Atualizar o schema para aceitar tanto o formato flat (specs simples) quanto o formato aninhado (specs com múltiplos tracks). Usar `oneOf` para suportar ambos.

---

### TD-03 — Spec Schema `templates` Paths Incorretos

| Field | Value |
|-------|-------|
| **Severidade** | Medium |
| **Esforço** | S |
| **Impacto** | Templates listados no spec.yaml não correspondem aos caminhos reais no disco |
| **Ação** | Fix Now |

**Descrição:** O `spec.yaml` lista templates como `discovery/template.md`, `specification/template.md`, etc. Mas os templates reais estão em `core/workflows/1-discovery/template.md`, `core/workflows/2-specification/template.md`. Os caminhos não batem.

**Evidência:** `specs/software/spec.yaml` linhas 43-47 vs. caminhos reais em `core/workflows/`.

**Recomendação:** Corrigir os caminhos no `spec.yaml` para apontar para os caminhos reais, ou definir claramente a convenção de resolução de caminhos no spec-loader.

---

### TD-04 — Diretório `core/tasks/` Vazio e Indefinido

| Field | Value |
|-------|-------|
| **Severidade** | Medium |
| **Esforço** | M |
| **Impacto** | Confusão sobre o papel do sistema de tasks; schema suporta mas nada existe |
| **Ação** | Plan Fix |

**Descrição:** O diretório `core/tasks/` existe mas está vazio. O `spec-schema.json` define `components.tasks` como um tipo de componente válido. Porém, nenhum task existe no projeto, nenhum workflow o referencia, e nenhum agente o consome. Não está claro se é um feature planejado ou abandonado.

**Evidência:** `ls core/tasks/` retorna vazio; `spec-schema.json` linha 71-77 define o campo.

**Recomendação:** Decidir: (a) implementar o sistema de tasks como unidades granulares dentro de workflows, ou (b) remover do schema e da estrutura para evitar confusão. Se implementar, definir claramente a diferença entre tasks e workflow steps.

---

### TD-05 — Model Profiles Configurados mas Não Consumidos

| Field | Value |
|-------|-------|
| **Severidade** | High |
| **Esforço** | M |
| **Impacto** | Feature de otimização de custo/qualidade existe na config mas não tem efeito |
| **Ação** | Plan Fix |

**Descrição:** `harnesskit.yaml` define 3 perfis de modelo (`quality`, `balanced`, `budget`) com mapeamento agente→modelo. O perfil ativo é `balanced`. Porém, nenhum agente, workflow ou engine doc referencia `model_profiles`. A configuração existe mas é decorativa.

**Evidência:** `harnesskit.yaml` linhas 57-78 definem os perfis. Nenhuma menção em nenhum arquivo `.agent.yaml`, `workflow-engine.md`, ou `state-machine.md`.

**Recomendação:** Integrar model profiles ao sistema. Quando Sheldon delega para um agente, o CLAUDE.md ou o prompt de ativação deveria indicar qual modelo usar baseado no perfil ativo. Isso permitiria ao usuário controlar custo vs. qualidade.

---

### TD-06 — Context Monitor Apenas Conceitual

| Field | Value |
|-------|-------|
| **Severidade** | High |
| **Esforço** | M |
| **Impacto** | Context rot não é prevenido; workflows longos degradam sem aviso |
| **Ação** | Plan Fix |

**Descrição:** O `context-monitor.md` descreve um sistema de monitoramento de contexto com níveis WARNING (40%) e CRITICAL (25%), e integração com checkpoints. Porém, não existe nenhuma implementação real — nenhum hook em `.claude/settings.json`, nenhuma verificação nos workflows, nenhum agente checa o nível de contexto.

**Evidência:** `core/engine/hooks/context-monitor.md` é documentação pura. Não existe `.claude/` directory no projeto (está no `.gitignore`).

**Recomendação:** Implementar como hook do Claude Code (`PostToolUse` ou similar) que injeta alertas no contexto quando o uso passa dos thresholds. Alternativamente, adicionar instruções nos agentes para auto-monitorar e criar checkpoints proativamente.

---

### TD-07 — Falta Workflow Dedicado para Tech-Debt-Audit

| Field | Value |
|-------|-------|
| **Severidade** | Medium |
| **Esforço** | M |
| **Impacto** | O step `tech-debt-audit` no state.json não tem workflow próprio; depende de instruções inline no agente |
| **Ação** | Plan Fix |

**Descrição:** O `state.json` define um step `tech-debt-audit` na fase de análise, e o `raj.agent.yaml` tem um behavior para ele. Porém, não existe um diretório `bf-1-analysis/tech-debt-audit/` com workflow, template e checklist dedicados. O workflow `bf-1-analysis/` cobre apenas `codebase-analysis`.

**Evidência:** `state.json` linha 17 define o step; `raj.agent.yaml` behaviors tem `tech-debt-audit`; mas `bf-1-analysis/` só contém um workflow (`codebase-analysis`).

**Recomendação:** Criar workflow dedicado em `bf-1-analysis/` com `tech-debt-workflow.yaml`, `tech-debt-template.md`, e `tech-debt-checklist.md`. Ou criar um subdiretório separado `bf-1-analysis-debt/`.

---

### TD-08 — Naming Inconsistente nos Workflows Brownfield

| Field | Value |
|-------|-------|
| **Severidade** | Low |
| **Esforço** | S |
| **Impacto** | Confusão na navegação; quebra o padrão de naming |
| **Ação** | Accept |

**Descrição:** Workflows brownfield usam prefixo `bf-` (`bf-1-analysis`, `bf-2-planning`, `bf-3-implementation`), mas a fase de review usa `5-review` (greenfield). Isso quebra o padrão de naming — deveria ser `bf-4-review` ou a convenção deveria ser documentada.

**Evidência:** `specs/software/spec.yaml` linha 41: `- 5-review/workflow.yaml` (no track brownfield).

**Recomendação:** Documentar explicitamente que a review é compartilhada entre greenfield e brownfield, ou criar um alias `bf-4-review/` que aponte para `5-review/`.

---

### TD-09 — Discovery Workflow Não Define `requirements` Step

| Field | Value |
|-------|-------|
| **Severidade** | High |
| **Esforço** | M |
| **Impacto** | Penny tem behavior para `requirements` mas não existe workflow definido para ele |
| **Ação** | Fix Now |

**Descrição:** O agente Penny define 3 workflows no menu: `brief`, `requirements`, e `stories`. O workflow em `1-discovery/workflow.yaml` cobre apenas o `project-brief`. Não existe um `requirements` workflow separado. Porém, o greenfield state precisaria de um step `requirements` na fase discovery, e Leonard consome `artifacts/discovery/requirements.md` como input obrigatório.

**Evidência:**
- `penny.agent.yaml` menu: trigger `requirements` → workflow `1-discovery/requirements`
- `1-discovery/workflow.yaml`: apenas `project-brief`
- `leonard.agent.yaml` consumes: `artifacts/discovery/requirements.md` (required)
- `3-architecture/workflow.yaml` inputs: `artifacts/discovery/requirements.md`

**Recomendação:** Criar o workflow `1-discovery/requirements-workflow.yaml` (ou adicionar como segundo workflow no diretório) com seu template e checklist. Este é um gap crítico no flow greenfield — sem ele, Leonard não tem input para a arquitetura.

---

### TD-10 — Discuss Workflow Output Path Sem Diretório

| Field | Value |
|-------|-------|
| **Severidade** | Medium |
| **Esforço** | S |
| **Impacto** | O workflow de discuss referencia `artifacts/discuss/` que não existe |
| **Ação** | Fix Now |

**Descrição:** O workflow `2.5-discuss` define output em `artifacts/discuss/implementation-vision.md`, mas o diretório `artifacts/discuss/` não existe na estrutura de diretórios (não tem nem `.gitkeep`).

**Evidência:** `2.5-discuss/workflow.yaml` linha 22: `path: "artifacts/discuss/implementation-vision.md"`. Diretório inexistente.

**Recomendação:** Criar `artifacts/discuss/.gitkeep`. Também verificar se `artifacts/analysis/`, `artifacts/planning/`, `artifacts/review/`, e `artifacts/discussions/` (party mode) existem.

---

### TD-11 — Party Mode Output Path Dinâmico Sem Diretório

| Field | Value |
|-------|-------|
| **Severidade** | Low |
| **Esforço** | S |
| **Impacto** | Party mode referencia `artifacts/discussions/` que não existe |
| **Ação** | Fix Now |

**Descrição:** O workflow `party-mode` define output em `artifacts/discussions/party-{{date}}.md`, mas o diretório `artifacts/discussions/` não existe.

**Evidência:** `party-mode/workflow.yaml` linha 43: `save_to: "artifacts/discussions/party-{{date}}.md"`.

**Recomendação:** Criar `artifacts/discussions/.gitkeep`.

---

### TD-12 — Workflow Actions Não Padronizadas

| Field | Value |
|-------|-------|
| **Severidade** | Medium |
| **Esforço** | M |
| **Impacto** | O workflow engine define 3 actions (ask, generate, checklist) mas workflows usam actions adicionais |
| **Ação** | Plan Fix |

**Descrição:** O `workflow-engine.md` define 3 tipos de action: `ask`, `generate`, e `checklist`. Porém, workflows reais usam actions adicionais não documentadas:
- `auto` (party-mode, step `select-agents`)
- `party` (party-mode, step `discussion`)

O engine não sabe como processar essas actions.

**Evidência:** `workflow-engine.md` seção 3 "Process Steps" define apenas `ask`, `generate`, `checklist`. `party-mode/workflow.yaml` usa `auto` e `party`.

**Recomendação:** Ou (a) documentar `auto` e `party` como actions válidas no workflow engine, ou (b) refatorar o party-mode para usar apenas as actions existentes (tratando `auto` como uma variante de `generate` e `party` como um loop de `ask`+`generate`).

---

## Summary Matrix

| ID | Finding | Severidade | Esforço | Ação |
|----|---------|------------|---------|------|
| TD-01 | Agent schema não reflete realidade | Critical | M | Fix Now |
| TD-02 | Spec schema workflows incompatível | High | S | Fix Now |
| TD-03 | Spec templates paths incorretos | Medium | S | Fix Now |
| TD-04 | core/tasks/ vazio e indefinido | Medium | M | Plan Fix |
| TD-05 | Model profiles não consumidos | High | M | Plan Fix |
| TD-06 | Context monitor conceitual | High | M | Plan Fix |
| TD-07 | Falta workflow tech-debt-audit | Medium | M | Plan Fix |
| TD-08 | Naming inconsistente brownfield review | Low | S | Accept |
| TD-09 | Falta workflow requirements | High | M | Fix Now |
| TD-10 | Discuss artifacts dir inexistente | Medium | S | Fix Now |
| TD-11 | Party mode artifacts dir inexistente | Low | S | Fix Now |
| TD-12 | Workflow actions não padronizadas | Medium | M | Plan Fix |

---

## Priorização Recomendada

### Quick Wins (Fix Now — esforço S)
1. TD-02 — Corrigir spec schema workflows
2. TD-03 — Corrigir spec templates paths
3. TD-10 — Criar artifacts/discuss/
4. TD-11 — Criar artifacts/discussions/

### Short-term (Fix Now — esforço M)
5. TD-01 — Reescrever agent schema
6. TD-09 — Criar workflow requirements

### Medium-term (Plan Fix)
7. TD-05 — Integrar model profiles
8. TD-06 — Implementar context monitor
9. TD-07 — Criar workflow tech-debt-audit
10. TD-12 — Padronizar workflow actions

### Accept / Monitor
11. TD-08 — Naming brownfield review (documentar)
12. TD-04 — Definir sistema de tasks (decidir se implementa ou remove)

---

## Next Steps

- [ ] Report reviewed and approved by the user
- [ ] Handoff created for the next phase (planning)
- [ ] State.json updated with status `completed`
