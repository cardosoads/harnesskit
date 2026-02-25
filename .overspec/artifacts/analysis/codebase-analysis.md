# Codebase Analysis: overspec-dev (Ciclo 2)

| Field    | Value                |
|----------|----------------------|
| Project  | overspec-dev         |
| Date     | 2026-02-25           |
| Version  | 2.0                  |
| Agent    | raj                  |
| Phase    | Analysis (Cycle 2)   |

---

## Objetivo do Ciclo

Adicionar um terceiro track ao framework: **New Features** — para adicionar features a projetos existentes que já passaram por um ciclo greenfield ou brownfield.

---

## Estado Atual do Framework (Pós-Ciclo 1)

O ciclo 1 corrigiu toda a dívida técnica identificada. O framework está internamente consistente:
- 44/44 checks de validação passando
- Schemas alinhados com a realidade
- Workflows completos para greenfield e brownfield
- Features (model profiles, context monitor) conectadas

---

## Arquitetura de Tracks Atual

O framework suporta 2 tracks:

| Track | Fases | Uso |
|-------|-------|-----|
| Greenfield | Discovery → Specification → Discuss (opt) → Architecture → Implementation → Review | Projeto novo do zero |
| Brownfield | Analysis → Planning → Implementation → Review | Corrigir/melhorar projeto existente |

**Gap identificado:** Não existe track para adicionar features novas a projetos que já existem. O brownfield é focado em tech debt, não em features.

---

## Arquivos que Precisam Mudar

### Configuração

| Arquivo | O que muda | Impacto |
|---------|-----------|---------|
| `overspec.yaml` | Adicionar `newfeatures_phases` | Define a estrutura do track |
| `state-machine.md` | Tornar lista de fases dinâmica (linha 77-81 hardcoded) | Suportar qualquer track |

### Agentes

| Arquivo | O que muda | Impacto |
|---------|-----------|---------|
| `sheldon.agent.yaml` | Adicionar 3ª opção em `project_type_detection`, atualizar phase map, atualizar `new_project_detection` | Sheldon reconhece e roteia o novo track |

### Spec & Workflows

| Arquivo | O que muda | Impacto |
|---------|-----------|---------|
| `spec.yaml` | Adicionar seção `newfeatures` em workflows e templates | Registrar novos workflows |
| Novos diretórios | Criar `nf-1-discovery/`, `nf-2-specification/`, `nf-3-architecture/`, `nf-4-implementation/` | Workflows do track |
| `5-review/` | Reutilizar (já é compartilhado gf/bf) | Sem mudança |

### Teams

| Arquivo | O que muda | Impacto |
|---------|-----------|---------|
| Novo `team-newfeatures.yaml` | Criar preset com penny, raj, leonard, howard, amy | Organização |

---

## Design Proposto: Track New Features

### Fases

```
1. Discovery (Raj + Penny)
   - Raj analisa o codebase existente e identifica onde a feature se encaixa
   - Penny levanta os requisitos da feature com o usuário

2. Specification (Penny)
   - Penny detalha os requisitos em user stories

3. Architecture (Leonard)
   - Leonard desenha como a feature se integra na arquitetura existente

4. Implementation (Howard)
   - Howard implementa as stories

5. Review (Amy)
   - Amy revisa com o protocolo de 3 níveis (reutiliza 5-review/)
```

### Diferenças do Greenfield

| Aspecto | Greenfield | New Features |
|---------|-----------|--------------|
| Discovery | Penny sozinha, projeto do zero | Raj mapeia o existente + Penny levanta requisitos |
| Architecture | Leonard cria do zero | Leonard adapta a arquitetura existente |
| Discuss | Opcional (2.5) | Não incluído (brainstorm é parte da discovery) |
| Review | Amy | Amy (compartilhado) |

### Workflows a Criar

```
core/workflows/
├── nf-1-discovery/
│   ├── workflow.yaml          # 2 sub-workflows: impact-analysis (raj) + feature-requirements (penny)
│   ├── impact-analysis-workflow.yaml
│   ├── impact-analysis-instructions.md
│   ├── impact-analysis-template.md
│   ├── impact-analysis-checklist.md
│   ├── feature-requirements-workflow.yaml
│   ├── feature-requirements-instructions.md
│   ├── feature-requirements-template.md
│   └── feature-requirements-checklist.md
├── nf-2-specification/
│   ├── workflow.yaml
│   ├── instructions.md
│   ├── template.md
│   └── checklist.md
├── nf-3-architecture/
│   ├── workflow.yaml
│   ├── instructions.md
│   ├── template.md
│   └── checklist.md
├── nf-4-implementation/
│   ├── workflow.yaml
│   ├── instructions.md
│   ├── template.md
│   └── checklist.md
└── 5-review/                  # Reutilizado
```

---

## Concerns

1. **state-machine.md hardcoded** — A lista de fases na linha 77-81 é hardcoded para greenfield. Precisa ser dinâmica para suportar qualquer track.
2. **Sheldon tem lógica binária** — O `project_type_detection` assume greenfield OU brownfield. Precisa suportar uma 3ª opção.
3. **Discovery com 2 agentes** — O Raj e a Penny na mesma fase é um padrão novo. Precisa definir como funciona a passagem de bastão dentro de uma fase.

---

## Next Steps

- [ ] Report reviewed and approved by the user
- [ ] Tech debt audit (não aplicável neste ciclo — foco é feature)
- [ ] Handoff to planning
