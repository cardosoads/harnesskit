# Validation Checklist: User Stories

Validate each item below against the generated user stories document. Items marked as **required** must pass for the document to be approved. Optional items are recommended but do not block approval.

---

## Required Items

- [ ] **All requirements covered** — Does every functional requirement from the requirements document have at least one corresponding user story?
  - Criterion: cross-reference the requirements list with the stories. No requirement should be left without a matching story.

- [ ] **Acceptance criteria present** — Does every user story have at least one acceptance criterion in Given/When/Then format?
  - Criterion: each story has a non-empty acceptance criteria section with at least one Given/When/Then block.

- [ ] **Priorities assigned** — Does every user story have a MoSCoW priority (Must-Have, Should-Have, Could-Have, Won't-Have)?
  - Criterion: the priority field is filled for every story.

- [ ] **No duplicate stories** — Are there any stories that describe the same functionality under different wording?
  - Criterion: no two stories have overlapping acceptance criteria or describe the same user action.

- [ ] **Valid story format** — Does every story follow the "As a [user], I want [action], so that [benefit]" format?
  - Criterion: all three components (persona, action, benefit) are present and meaningful.

---

## Optional Items (recommended)

- [ ] **Complexity estimated** — Does every story have a complexity estimate (S/M/L)?
  - Criterion: the complexity field is filled for every story.

- [ ] **Dependencies identified** — Are inter-story dependencies documented where they exist?
  - Criterion: stories that require other stories to be completed first have this noted.

- [ ] **Epics are balanced** — Are stories reasonably distributed across epics (no epic with 80% of all stories)?
  - Criterion: no single epic contains more than 50% of the total stories.

- [ ] **User personas consistent** — Do the user personas in the stories match the profiles defined in the brief?
  - Criterion: every "As a [user]" references a persona defined in the project brief.

---

## Validation Result

- **All required items approved?** -> Document approved. Proceed to handoff.
- **Any required item failed?** -> Inform the user which item failed and go back to the corresponding step to fix it.
- **Optional items failed?** -> Inform the user, suggest filling them in, but do not block progress.
