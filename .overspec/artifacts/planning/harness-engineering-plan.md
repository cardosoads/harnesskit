# Plano de Harness Engineering para o OverSpec

## Objetivo

Evoluir o OverSpec de um framework artifact-driven/spec-driven para um harness de agentes: um sistema que fornece contexto, estado, contratos, sensores e ciclos de correcao para permitir execucoes longas com menor degradacao de qualidade.

Este plano parte de cinco fontes:

- OpenAI: https://openai.com/pt-BR/index/harness-engineering/
- Anthropic: https://www.anthropic.com/engineering/harness-design-long-running-apps
- Martin Fowler: http://martinfowler.com/articles/harness-engineering.html
- TLC Spec Driven: https://agent-skills.techleads.club/skills/tlc-spec-driven/
- GSD 2: https://github.com/gsd-build/gsd-2

## Sintese dos conceitos

### 1. Harness nao e so prompt

O harness e o ambiente operacional ao redor do modelo. Ele inclui:

- guias de contexto antes da execucao;
- estado versionado no repositorio;
- planos e progresso persistidos;
- testes, linters e verificadores estruturais;
- avaliadores separados do agente implementador;
- loops de correcao;
- coleta recorrente de drift e divida tecnica.

No OverSpec, isso ja existe parcialmente por meio de `state.json`, agentes, workflows, handoffs e artefatos. A lacuna esta em transformar esses artefatos em um loop verificavel com sensores e contratos.

### 2. Feedforward e feedback

Feedforward orienta o agente antes de gerar codigo:

- `CLAUDE.md`;
- `.overspec/core/constitution.md`;
- specs;
- artefatos de discovery, specification e architecture;
- guias de estilo;
- planos de implementacao.

Feedback mede o resultado depois:

- lint;
- typecheck;
- testes unitarios;
- testes de integracao;
- testes de UI;
- verificacao de arquitetura;
- review agent;
- checagens de artefatos;
- score de qualidade.

O OverSpec hoje e mais forte em feedforward. O MVP de harness deve focar em feedback mecanico e no loop implementador -> avaliador -> corretor.

### 3. Conhecimento do repositorio como sistema de registro

O `AGENTS.md` ou `CLAUDE.md` nao deve virar um manual gigante. Ele deve funcionar como indice. O conhecimento pesado deve ficar distribuido em documentos locais, versionados e verificaveis.

Para o OverSpec, a direcao e:

- manter `CLAUDE.md` curto;
- usar `.overspec/core/` como regras centrais;
- usar `.overspec/artifacts/` como memoria de execucao;
- criar um indice de contexto para guiar agentes ao artefato certo;
- adicionar checks que detectem artefatos obsoletos, vazios ou desconectados.

### 4. Avaliador separado e custo adaptativo

A Anthropic mostra que um avaliador separado vale mais quando a tarefa esta no limite da capacidade do modelo. Para tarefas simples, pode virar overhead.

No OverSpec, a regra deve ser adaptativa:

- tarefa simples: sensores computacionais obrigatorios, sem avaliador LLM por padrao;
- tarefa media: sensores computacionais + Amy revisando contrato e resultados;
- tarefa complexa: Howard implementa, Amy valida em processo separado, Sheldon orquestra retries;
- tarefa critica: incluir humano como gate explicito.

### 5. Drift e coleta de lixo

A OpenAI destaca que agentes replicam padroes ruins existentes e geram drift com o tempo. Isso exige checks recorrentes, nao apenas revisao no final de uma feature.

No OverSpec, isso vira uma rotina de manutencao:

- detectar artefatos desatualizados;
- detectar debt entries recorrentes;
- detectar duplicacao de regras;
- verificar aderencia a arquitetura;
- abrir plano de correcao pequeno e especifico.

## Problemas que a ferramenta deve resolver

1. Agente tenta executar escopo grande demais em uma unica janela.
2. Agente declara pronto sem validar comportamento real.
3. Nova sessao perde contexto do que foi feito e do que falhou.
4. Review vira julgamento subjetivo do mesmo agente que implementou.
5. Testes e linters sao recomendados, mas nao bloqueiam progresso.
6. Artefatos existem, mas podem ser stubs ou estar desconectados.
7. Arquitetura deriva aos poucos a cada ciclo.
8. Custo aumenta sem visibilidade de retorno por fase.
9. Falhas recorrentes nao voltam para o sistema como regras ou sensores.

## Proposta de arquitetura

### Diretorios novos

```text
.overspec/
  harness/
    HARNESS.md
    sensors.yaml
    contracts/
      active/
      completed/
    evaluations/
    progress/
    drift/
```

### Artefatos principais

| Artefato | Papel |
| --- | --- |
| `harness/HARNESS.md` | Indice do harness: como rodar, quais sensores existem e quando usar Amy |
| `harness/sensors.yaml` | Lista de sensores computacionais por projeto e fase |
| `harness/contracts/active/<id>.md` | Contrato entre implementador e avaliador antes da execucao |
| `harness/contracts/completed/<id>.md` | Contrato fechado com resultado final |
| `harness/evaluations/<id>.md` | Resultado da avaliacao: checks, evidencias, falhas, score |
| `harness/progress/<id>.md` | Memoria curta por unidade de trabalho |
| `harness/drift/<date>.md` | Resultado de manutencao recorrente |

## Modelo de contrato

Cada implementacao relevante deve gerar um contrato antes do codigo:

```yaml
id: HC-0001
source_spec: artifacts/specification/feature-stories.md
source_design: artifacts/architecture/feature-design.md
owner_builder: howard
owner_evaluator: amy
risk: medium
must_haves:
  - id: MH-01
    truth: "Comportamento observavel esperado"
    files_expected:
      - "path/to/file"
    verification:
      - "npm run test"
  - id: MH-02
    truth: "Artefato real, nao stub"
    verification:
      - "static-review"
blockers:
  - "Nenhum requisito aberto"
exit_criteria:
  min_score: 0.85
  required_sensors_pass: true
```

## Sensores

### Sensores computacionais

Devem ser preferidos quando houver uma resposta objetiva.

Exemplos:

- `npm run lint`
- `npm run test`
- `npm run typecheck`
- `pytest`
- `pnpm test:e2e`
- `depcruise`
- `semgrep`
- script customizado para limites arquiteturais
- script customizado para detectar placeholders em artefatos

### Sensores inferenciais

Devem ser usados quando ha julgamento semantico.

Exemplos:

- Amy revisa se a implementacao cumpre o contrato;
- Amy identifica stub visual ou feature display-only;
- Raj faz auditoria de tech debt;
- Sheldon decide se uma falha exige pergunta humana.

## Loop de execucao

```text
1. Sheldon identifica proxima unidade de trabalho.
2. Leslie guia a criacao do contrato com must-haves verificaveis.
3. Amy revisa o contrato antes da implementacao quando o risco exigir.
4. Howard implementa em escopo de uma janela de contexto.
5. Sensores computacionais rodam automaticamente.
6. Amy avalia resultado contra o contrato, se o risco justificar.
7. Se falhar: Sheldon reabre rodada de correcao com feedback objetivo.
8. Se passar: contrato e movido para completed, progresso e atualizado.
9. Falhas recorrentes viram regra, sensor ou documentacao.
```

## MVP proposto

### Fase 1: Harness passivo

Criar estrutura de arquivos, templates e convencoes:

- `harness/HARNESS.md`;
- `harness/sensors.yaml`;
- template de contrato;
- template de avaliacao;
- template de progresso;
- atualizacao do workflow de implementacao para exigir contrato.

Resultado esperado: o OverSpec passa a registrar contratos e avaliacoes sem ainda automatizar retries.

### Fase 2: Gate de sensores

Adicionar um passo obrigatorio no workflow de implementacao:

- ler `sensors.yaml`;
- rodar comandos configurados;
- salvar resultado em `harness/evaluations/`;
- bloquear "completed" se sensor obrigatorio falhar.

Resultado esperado: o agente nao pode marcar pronto apenas por julgamento proprio.

### Fase 3: Builder/Evaluator loop

Separar formalmente:

- Howard: implementador;
- Amy: avaliadora;
- Sheldon: orquestrador de retries.

Resultado esperado: falhas de Amy voltam para Howard como input objetivo, ate passar ou escalar para humano.

### Fase 4: Drift collection

Adicionar workflow recorrente de manutencao:

- revisar duplicacao;
- revisar artefatos obsoletos;
- revisar padroes arquiteturais violados;
- gerar plano pequeno de correcao.

Resultado esperado: reduzir slop acumulado.

## Diferenca em relacao ao GSD 2

O GSD 2 e mais orientado a auto-mode completo, com hierarquia milestone -> slice -> task, sessoes limpas por unidade, verificacao, recovery e controle de custo.

O OverSpec pode se diferenciar por:

- ser mais artifact-driven e multi-agente por design;
- permitir modo colaborativo mais guiado;
- ter Amy como gate de qualidade semantica;
- manter contratos formais entre builder e evaluator;
- priorizar adaptabilidade por risco em vez de sempre rodar tudo.

## Diferenca em relacao ao TLC Spec Driven

Spec Driven resolve bem o feedforward: escopo, historias, criterios de aceite e divisao de tarefas.

O harness do OverSpec deve adicionar:

- sensores obrigatorios;
- estado de progresso entre sessoes;
- avaliador separado;
- contratos antes da implementacao;
- drift checks depois da integracao;
- loop de correcao com evidencias.

## Decisao recomendada

Construir a ferramenta como uma evolucao do OverSpec, nao como um CLI separado no primeiro momento.

Primeiro entregar templates e workflow de contrato/avaliacao. Depois adicionar automacao de sensores e retries. Isso reduz risco porque o OverSpec ja tem os conceitos centrais: agentes, estado, fases, handoffs e artefatos.

## Status de implementacao

### Fase 1 concluida em 2026-04-13

Entregue:

- `.overspec/harness/HARNESS.md`
- `.overspec/harness/sensors.yaml`
- templates de contrato, avaliacao, progresso e drift
- diretorios para contratos ativos/concluidos, avaliacoes, progresso e drift
- workflows de implementacao atualizados para criar contrato e registrar sensores
- templates de relatorio atualizados com contrato e evidencia de sensores
- checklists de implementacao atualizados para bloquear entrega sem harness
- workflow de review atualizado para Amy revisar contrato e sensores
- agentes Howard e Amy atualizados com principios de harness
- `workflow-engine.md` atualizado com regras gerais de harness
- `validate.sh` atualizado para exigir arquivos e diretorios centrais do harness

Ainda nao entregue:

- execucao automatica de sensores
- retry loop Howard -> Amy -> Sheldon
- movimentacao automatica de contratos de `active/` para `completed/`
- score automatico de avaliacao
- workflow recorrente de drift collection

### Fase 2 parcialmente concluida em 2026-04-13

Entregue:

- `.overspec/harness/feedforward.yaml` para declarar contexto minimo verificavel
- `.overspec/scripts/harness_doctor.py` para checar feedforward e feedback
- `.overspec/scripts/harness-doctor.sh` como wrapper executavel
- `harness-doctor` adicionado como sensor obrigatorio em `sensors.yaml`
- `overspec-validate` tornado sensor obrigatorio de implementacao
- `validate.sh` atualizado para exigir `feedforward.yaml` e o doctor
- `HARNESS.md` atualizado com o protocolo do doctor

O doctor agora identifica:

- arquivos centrais de contexto ausentes;
- specs ativas ausentes;
- time ativo ausente;
- fases configuradas que nao aparecem no `state.json`;
- artefatos registrados no `state.json` que nao existem;
- artefatos rasos ou com marcadores de template/TODO;
- steps concluidos sem artefato;
- workflows de implementacao sem contrato/sensor;
- relatorios de implementacao sem secao de harness;
- sensores obrigatorios ausentes;
- test runners detectados sem sensor correspondente;
- contratos ativos/concluidos sem avaliacao.

Ideias incorporadas do GSD 2:

- doctor estrutural com severidades;
- separacao entre estado em disco e sessao do agente;
- must-haves mecanicamente verificaveis;
- verificacao como gate explicito;
- checks auto-descobertos em modo informativo/advisory quando ainda nao sao obrigatorios;
- unidade de trabalho pequena o suficiente para caber em uma janela de contexto.

Lacunas detectadas no estado atual:

- `design` esta configurado para o track `new-features`, mas nao aparece em `state.json`;
- `feature-implementation` esta marcado como concluido sem artefato;
- `feature-design.md` contem marcadores Handlebars/TODO em linhas especificas;
- `bf-setup-report.md` e anterior ao harness e nao tem secao `Harness Contract`;
- nao ha `package.json`, `pyproject.toml` ou `pytest.ini`, entao o feedback de codigo esta limitado aos sensores estruturais do OverSpec.

Ainda nao entregue:

- execucao automatica com retry;
- promocao automatica de contratos `active` para `completed`;
- UAT/human review script gerado a partir do contrato;
- reconciliacao de marco/feature comparando sucesso planejado versus resultado final.

### Fase 2.1 concluida em 2026-04-13

Entregue:

- `.overspec/core/agents/leslie.agent.yaml` como agente dono da criacao de contratos;
- `.overspec/core/workflows/harness-contract/` como fluxo guiado para transformar uma unidade de trabalho em contrato verificavel;
- `spec.yaml` e times atualizados para incluir Leslie antes da implementacao;
- Sheldon atualizado para delegar pedidos de contrato para Leslie;
- Howard atualizado para preferir Leslie antes de editar codigo;
- party mode atualizado para usar Leslie em discussoes de contrato, verificabilidade e sensores;
- `HARNESS.md`, `workflow-engine.md`, `feedforward.yaml` e `validate.sh` atualizados para tratar Leslie e o workflow de contrato como parte central do harness.

O fluxo passa a ser: Sheldon identifica a unidade de trabalho, Leslie guia e salva o contrato, Howard implementa contra o contrato, Amy avalia quando o risco exigir.

### Fase 2.2 concluida em 2026-04-13

Entregue:

- `.overspec/scripts/harness_evaluate.py` como runner mecanico de avaliacao;
- `.overspec/scripts/harness-evaluate.sh` como wrapper executavel;
- geracao de avaliacao Markdown em `.overspec/harness/evaluations/`;
- selecao explicita de contrato ou uso do contrato ativo mais recente;
- execucao dos sensores obrigatorios de `implementation`;
- registro de sensores recomendados como `SKIPPED` por padrao;
- veredito `BLOCKED` quando sensor obrigatorio falha, expira ou esta indisponivel;
- documentacao do runner em `.overspec/harness/HARNESS.md`;
- `validate.sh` atualizado para exigir runner e wrapper;
- grupo `harness_evaluation` em `.overspec/harness/sensors.yaml`.

Ainda nao entregue:

- retry automatico Howard -> Amy -> Howard;
- promocao automatica de contratos `active` para `completed`;
- UAT/human review script gerado a partir do contrato;
- reconciliacao de marco/feature comparando sucesso planejado versus resultado final.

### Fase 2.3 concluida em 2026-04-13

Entregue:

- `.overspec/harness/baselines/current.yaml` para registrar findings conhecidos;
- `.overspec/harness/baselines/README.md` com politica de baseline;
- `harness_doctor.py` atualizado para reclassificar findings nao-erro como
  `BASELINE` quando casam por `plane`, `code`, `file` e `message_contains`;
- `--format json` do doctor agora expoe `baseline` em cada issue aceita;
- `validate.sh` atualizado para exigir baseline policy;
- `HARNESS.md` atualizado com regras de baseline.

Ainda nao entregue:

- retry automatico Howard -> Amy -> Howard;
- promocao automatica de contratos `active` para `completed`;
- expiracao automatica de baseline;
- comando para gerar baseline entries automaticamente;
- UAT/human review script gerado a partir do contrato;
- reconciliacao de marco/feature comparando sucesso planejado versus resultado final.
