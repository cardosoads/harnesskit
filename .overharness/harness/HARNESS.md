# OverHarness Harness

Este diretorio define a camada de Harness Engineering do OverHarness.

O objetivo do harness e envolver os agentes com contexto, contratos, sensores,
memoria curta e criterios de avaliacao. Ele nao substitui specs, agentes ou
workflows; ele adiciona controle operacional ao que ja existe.

## Principios

> Decisao operacional 2026-04-13: a partir deste ponto, o Harness e prioridade
> para qualquer nova feature do OverHarness. Nenhuma feature nao trivial deve ir
> para Howard sem contrato ativo guiado por Leslie.

1. **Contrato antes de codigo**
   Cada implementacao relevante deve gerar um contrato em
   `contracts/active/` antes de alterar codigo. O contrato descreve o que
   precisa ser verdadeiro no final, quais arquivos devem existir ou mudar, e
   quais sensores verificam o resultado.

2. **Sensores antes de julgamento**
   O agente implementador nao deve ser o unico juiz do proprio trabalho.
   Sempre que houver um sensor objetivo, ele vem antes de avaliacao semantica.

3. **Avaliador por risco**
   Amy deve revisar contratos e resultados quando o risco for medio, alto ou
   critico. Para tarefas simples, sensores computacionais podem ser suficientes.

4. **Memoria curta por unidade**
   Cada unidade de trabalho deve registrar progresso em `progress/`. Uma nova
   sessao deve conseguir continuar sem depender do historico do chat.

5. **Falhas viram melhoria do harness**
   Falhas recorrentes devem virar regra, sensor, template ou documentacao.
   O objetivo e reduzir o mesmo tipo de erro nas proximas execucoes.

## Estrutura

```text
.overharness/harness/
  HARNESS.md
  feedforward.yaml
  sensors.yaml
  templates/
    contract-template.md
    evaluation-template.md
    progress-template.md
    drift-template.md
  baselines/
    README.md
    current.yaml
  contracts/
    active/
    completed/
  evaluations/
  progress/
  drift/
```

## Loop padrao

```text
1. Sheldon identifica a proxima unidade de trabalho.
2. Leslie guia a criacao do contrato em contracts/active/.
3. Amy revisa o contrato quando o risco justificar.
4. Howard implementa apenas o escopo do contrato.
5. Howard registra progresso em progress/.
6. Howard executa os sensores configurados em sensors.yaml.
7. Amy avalia o resultado contra o contrato quando necessario.
8. Falhas voltam para Howard como input objetivo.
9. Quando aprovado, o contrato vai para contracts/completed/.
```

## Politica de risco

| Risco | Exemplo | Politica |
| --- | --- | --- |
| `low` | Mudanca pequena, sem arquitetura nova, poucos arquivos | Sensores computacionais; Amy opcional |
| `medium` | Feature com multiplos arquivos ou comportamento usuario-visivel | Sensores + Amy revisa resultado |
| `high` | Mudanca de arquitetura, dados, auth, billing, migrations | Amy revisa contrato antes e depois |
| `critical` | Seguranca, perda de dados, producao, pagamentos | Amy + decisao humana obrigatoria |

## Relacao com os workflows

Os workflows de implementacao devem:

- ler este arquivo antes de implementar;
- delegar a criacao do contrato para Leslie usando `core/workflows/harness-contract/`;
- consultar `sensors.yaml`;
- salvar evidencia de sensores no relatorio de implementacao;
- bloquear conclusao se um sensor obrigatorio falhar;
- documentar desvios em contrato e relatorio.

## Doctor verificavel

Use `bash .overharness/scripts/harness-doctor.sh` para checar prontidao de
feedforward e feedback.

O doctor reporta:

- specs, times, workflows e arquivos centrais ausentes;
- artefatos registrados no `state.json` que nao existem;
- artefatos muito rasos ou com placeholders;
- etapas concluidas sem artefato;
- workflows de implementacao sem contrato ou sensor;
- sensores obrigatorios ausentes;
- checks descobertos no projeto que nao estao configurados;
- contratos ativos sem avaliacao.
- baseline accepted findings quando uma divida conhecida esta registrada em
  `baselines/current.yaml`.

Se houver erro, o harness nao deve avancar automaticamente. Avisos devem ser
tratados como divida operacional: podem nao bloquear uma correcao pequena, mas
devem virar contrato, sensor, artefato ou decisao explicita.

## Baselines

Use `.overharness/harness/baselines/current.yaml` para documentar avisos conhecidos
que pertencem ao baseline historico do projeto.

Regras:

- baselines nao ocultam erros;
- baselines so reclassificam findings que casam por `plane`, `code` e `file`;
- `message_contains` deve ser usado para deixar o match mais estreito;
- `expires_at` e obrigatorio no formato `YYYY-MM-DD`;
- baseline vencida, ausente ou invalida nao reclassifica o finding;
- qualquer finding novo que nao casar com a baseline continua aparecendo como
  warning;
- cada baseline precisa ter motivo, dono e follow-up.

## Runner de avaliacao

Use `bash .overharness/scripts/harness-evaluate.sh` para executar os sensores de
um contrato ativo e gravar uma avaliacao duravel em `evaluations/`.

Exemplos:

```bash
bash .overharness/scripts/harness-evaluate.sh --help
bash .overharness/scripts/harness-evaluate.sh --contract .overharness/harness/contracts/active/HC-YYYYMMDD-slug.md
bash .overharness/scripts/harness-evaluate.sh --include-recommended
```

Comportamento:

- se `--contract` nao for informado, o runner usa o contrato ativo mais recente;
- por padrao, executa os sensores obrigatorios do grupo `implementation`;
- sensores recomendados sao registrados como `SKIPPED`, a menos que
  `--include-recommended` seja usado;
- qualquer sensor obrigatorio que falhar, expirar ou estiver indisponivel
  bloqueia a avaliacao com veredito `BLOCKED`;
- o runner nao altera `state.json` e nao move contratos para `completed/`.
