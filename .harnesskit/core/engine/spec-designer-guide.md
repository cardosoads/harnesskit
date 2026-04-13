# Harnesskit Spec Designer Guide

## Overview

The Spec Designer (Bernadette) can analyze any domain and generate a
complete spec with agents, workflows, and templates.

## Design Process

### Step 1: Input Analysis
Bernadette accepts input in several forms:
- Documentation files (PRDs, READMEs, wikis)
- Domain descriptions (verbal or written)
- Existing project code (for brownfield specs)
- Reference specs (to extend or adapt)

### Step 2: Domain Decomposition
From the input, Bernadette extracts:
- **Entities**: Key objects/concepts in the domain (e.g., Order, Customer, Campaign)
- **Workflows**: Processes that transform entities (e.g., create-order, launch-campaign)
- **Stakeholders**: People/roles involved (e.g., Developer, Marketing Manager, Data Analyst)
- **Integrations**: External systems (e.g., APIs, databases, services)

### Step 3: Agent Recommendation
For each stakeholder/role, Bernadette recommends an agent:
- Agent ID (kebab-case)
- Agent name (persona name)
- Title and role description
- Confidence score (0.0 - 1.0):
  - 0.9-1.0: Strong evidence from docs, clearly needed
  - 0.7-0.8: Good evidence, likely needed
  - 0.5-0.6: Moderate evidence, may be optional
  - Below 0.5: Speculative, needs user validation

### Step 4: Workflow Design
For each agent, Bernadette designs:
- Workflows they participate in
- Templates they produce
- Checklists for validation

### Step 5: Spec Generation
After user approval, Bernadette generates:
- spec.yaml (manifest)
- agents/*.agent.yaml (one per agent)
- workflows/*/workflow.yaml + instructions.md + template.md + checklist.md
- teams/team-{name}.yaml (default team for this spec)

## Example: Designing a Marketing Spec

Input: "I need a spec for managing digital marketing campaigns"

Bernadette's analysis:
| Entity | Description |
|--------|------------|
| Campaign | A marketing campaign with budget, timeline, channels |
| Audience | Target audience segments |
| Content | Creative assets (copy, images, videos) |
| Channel | Distribution channels (social, email, ads) |
| Metric | KPIs and performance data |

Recommended agents:
| Agent | Title | Confidence |
|-------|-------|-----------|
| strategist | Campaign Strategist | 0.95 |
| creative | Content Creator | 0.90 |
| analyst | Performance Analyst | 0.85 |
| channel-manager | Channel Manager | 0.70 |

Recommended phases:
1. Strategy → 2. Content Creation → 3. Distribution → 4. Analysis → 5. Optimization

## Persona Naming Convention

When designing agents for new specs, Bernadette should:
- Give each agent a human name (like the BBT characters in the software spec)
- Match the personality to the role (e.g., a data analyst could be meticulous like Amy)
- Include a catchphrase that captures their perspective
- Keep names thematic within the spec (all from same show/universe, or all from a domain)

## Spec Validation

After generation, validate:
- [ ] spec.yaml passes schema validation
- [ ] All component files exist
- [ ] Agent IDs are unique and kebab-case
- [ ] Workflows reference valid agents
- [ ] No overlap in agent responsibilities
- [ ] Confidence scores are documented
