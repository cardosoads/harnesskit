# Harnesskit Context Monitor

## Purpose
Monitors context window usage during agent execution and triggers
warnings to prevent context rot — the degradation of output quality
when the context window fills up.

## Alert Levels

| Level | Remaining Context | Action |
|-------|------------------|--------|
| NORMAL | > 40% | No action needed |
| WARNING | 25-40% | Inject warning to agent: "Context at [X]%. Consider wrapping up current step or creating a checkpoint." |
| CRITICAL | < 25% | Inject critical alert: "CRITICAL: Context at [X]%. You MUST create a checkpoint NOW and save all progress to state.json before context degrades." |

## How It Works

1. After each tool use, estimate remaining context capacity
2. If below WARNING threshold: inject a system-level note to the agent
3. If below CRITICAL threshold: inject urgent instruction to checkpoint
4. Agent must follow checkpoint protocol from workflow-engine.md

## Integration with Agents

All agents must be aware of context monitoring:
- When receiving a WARNING: finish the current step, save progress
- When receiving CRITICAL: immediately save all collected data to
  state.json, create a checkpoint, and signal that a fresh agent
  should continue

## Artifact Size Guidelines

To minimize context waste, artifacts should follow size limits:

| Artifact | Max Size | Rationale |
|----------|----------|-----------|
| Project Brief | ~500 words | Concise overview, not a novel |
| Requirements | ~1000 words | Enough detail, not exhaustive prose |
| Architecture | ~1500 words | Components + decisions, not a textbook |
| User Stories | ~100 words/story | Given/When/Then, not essays |
| Review Report | ~800 words | Findings + verdict, not commentary |
| state.json | < 100 lines | State, not history |

## Implementation Notes

For Claude Code: this can be implemented as a PostToolUse hook in
.claude/settings.json or hooks configuration.

For other IDEs: equivalent monitoring should be configured per platform.
