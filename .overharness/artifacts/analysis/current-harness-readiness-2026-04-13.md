# Analise atual do OverHarness com Harness

| Campo | Valor |
| --- | --- |
| Projeto | overharness-dev |
| Data | 2026-04-13 |
| Tipo | new-features |
| Time ativo | team-newfeatures |
| Sensor principal | `bash .overharness/scripts/harness-doctor.sh` |
| Status | Pronto para proximo ciclo com divida operacional conhecida |

## Resumo

O OverHarness esta em bom estado para evoluir o Harness, mas o estado atual mistura
um ciclo antigo concluido antes do Harness com a nova camada de contratos,
sensores e avaliacao. A estrutura nova esta presente e valida; os problemas
atuais estao concentrados em rastreabilidade de artefatos antigos e em falta de
sensores de codigo, nao em quebra estrutural do framework.

A partir desta analise, qualquer nova feature do OverHarness deve usar o Harness
como gate padrao: Sheldon identifica a unidade de trabalho, Leslie guia e salva
o contrato, Howard implementa contra esse contrato, sensores rodam antes da
conclusao, e Amy revisa quando o risco for medio, alto ou critico.

## Resultado dos sensores

### `validate.sh`

Resultado: passou.

- 72 itens checados.
- 72 itens passaram.
- 1 aviso: `ajv-cli` nao esta instalado, entao o script pulou validacao de
  schema via CLI.
- Validacao complementar com `jsonschema` confirmou 9 agentes validos contra
  `.overharness/core/agents/_schema.json`.

### `harness-doctor`

Resultado: 0 erros, 4 avisos, 1 informativo.

Avisos:

- `design` esta configurado em `overharness.yaml`, mas nao aparece em
  `.overharness/state.json`.
- `.overharness/artifacts/architecture/feature-design.md` contem marcadores de
  template nas linhas 239, 303, 304, 305 e 319.
- O step `implementation/feature-implementation` esta concluido em
  `state.json`, mas sem artefato registrado.
- `.overharness/artifacts/implementation/bf-setup-report.md` e anterior ao Harness
  e nao tem secao `Harness Contract`.

Informativo:

- Nao ha `package.json`, `pyproject.toml` ou `pytest.ini`; por isso, o feedback
  atual esta limitado a sensores estruturais do OverHarness.

## Estado atual

O `state.json` registra o ciclo 4 como concluido, com `current_phase` igual a
`completed`. Isso significa que uma nova feature deve abrir uma nova unidade de
trabalho, nao continuar implicitamente o ciclo anterior.

Artefatos existentes e utilizaveis:

- `.overharness/artifacts/analysis/codebase-analysis.md`
- `.overharness/artifacts/analysis/tech-debt-report.md`
- `.overharness/artifacts/planning/improvement-plan.md`
- `.overharness/artifacts/planning/harness-engineering-plan.md`
- `.overharness/artifacts/discovery/impact-analysis.md`
- `.overharness/artifacts/discovery/feature-requirements.md`
- `.overharness/artifacts/specification/feature-stories.md`
- `.overharness/artifacts/architecture/feature-design.md`
- `.overharness/artifacts/implementation/bf-setup-report.md`
- `.overharness/artifacts/review/review-report.md`

O Harness novo esta presente:

- `.overharness/harness/HARNESS.md`
- `.overharness/harness/feedforward.yaml`
- `.overharness/harness/sensors.yaml`
- `.overharness/harness/templates/contract-template.md`
- `.overharness/core/agents/leslie.agent.yaml`
- `.overharness/core/workflows/harness-contract/`
- `.overharness/scripts/harness_doctor.py`
- `.overharness/scripts/harness-doctor.sh`

Ainda nao ha contratos ativos, avaliacoes ou progresso preenchidos em
`.overharness/harness/`; apenas os diretorios e templates existem.

## Como prosseguir

### Caminho recomendado imediato

1. Fechar a integracao inicial do Harness atual como uma unidade de trabalho
   revisavel.
2. Criar um contrato Leslie para a proxima melhoria concreta, antes de alterar
   qualquer workflow novo.
3. Usar `harness-doctor` como sensor obrigatorio em toda implementacao.
4. Manter `validate.sh` como sensor obrigatorio.
5. Fazer Amy revisar toda mudanca de risco `medium` ou maior.

### Primeira feature recomendada

Implementar o runner de avaliacao do Harness:

- entrada: contrato ativo em `.overharness/harness/contracts/active/`;
- execucao: sensores exigidos por `.overharness/harness/sensors.yaml`;
- saida: avaliacao em `.overharness/harness/evaluations/`;
- regra: bloquear conclusao quando sensor obrigatorio falhar sem baseline
  aprovado;
- handoff: Amy recebe contrato, resultados dos sensores e desvios.

Por que esta deve vir primeiro: o Harness ja possui contrato, sensores e doctor,
mas ainda nao tem o runner que transforma esses elementos em um loop executavel.
Sem isso, o gate existe como regra e artefato; com isso, vira mecanismo.

### Dividas que devem virar contratos pequenos

- Corrigir ou remover placeholders residuais em
  `.overharness/artifacts/architecture/feature-design.md`.
- Reconciliar `state.json` com a fase opcional `design`.
- Registrar artefato para `implementation/feature-implementation` ou documentar
  a excecao historica.
- Decidir se artefatos antigos, como `bf-setup-report.md`, devem receber uma
  secao retroativa de Harness ou permanecer como baseline pre-Harness.
- Adicionar sensores de codigo quando existir um runtime real para testar.

## Regra operacional

Nova feature do OverHarness agora segue este gate:

```text
Sheldon -> Leslie -> Howard -> sensores -> Amy
```

Para trabalho grande ou ambiguo, antes de Leslie entram Raj, Penny e Leonard:

```text
Raj -> Penny -> Leonard -> Leslie -> Howard -> sensores -> Amy
```

Se a mudanca for pequena, documentada e sem risco arquitetural, o caminho pode
ser encurtado para:

```text
Sheldon -> Leslie contrato leve -> Howard -> validate.sh + harness-doctor
```

Mesmo no caminho curto, o contrato de Leslie continua sendo o gate padrao para
features novas.
