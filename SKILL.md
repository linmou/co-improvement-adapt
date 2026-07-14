---
name: co-improvement-adapt
description: Use when a task must be adapted into a reusable human-AI co-improvement workflow or local Codex skill, with mandatory draft persistence, human checkpoints, rubric scoring, memory append generation, and post-loop reflection. Use when the user asks to turn .co-improvement results, project learnings, review workflows, or repeated human-in-the-loop procedures into a reusable workflow or skill.
---

# Human-AI Co-Improvement Task Adapter

## Core Principle
Run one mandatory human-in-the-loop pipeline in the same dialogue: align, draft, co-review, persist learnings, reflect.

## Two-Level Loop Semantics
The loop is meaningful at two scopes:
- Meta-adaptation scope: while this skill adapts a workflow, run the co-improvement lifecycle so the adaptation artifact, the human, and the AI all improve during the adaptation work.
- Embedded workflow scope: the adapted workflow produced by this skill must itself include a co-improvement lifecycle so future executions of that workflow improve the work output, the human, and the AI during the target task.

These scopes are nested, not infinitely recursive. Run the meta-adaptation loop over the draft artifact now; design the embedded loop as a required part of the adapted workflow blueprint.

## Local Skill Output Mode
Default to producing a local Codex skill when the adapted workflow is reusable beyond the current conversation, the user asks for a "skill", or the workflow should be invoked later by `$skill-name`.

Read `references/local-skill-output.md` before drafting or modifying a local skill. The produced skill must contain explicit space for human-in-the-loop improvement: alignment checkpoints, representative edits or work samples, co-review, memory persistence, reflection, and future iteration notes.

If the user explicitly wants only a draft workflow, persist the workflow under `./.co-improvement/drafts/` and skip local skill scaffolding with a stated reason.

## Non-Negotiable Rules
1. Require a clear task. If unclear, respond exactly: "Please provide a specific task or description to adapt." and stop.
2. Read memory files first if present:
   - User-global: `~/.codex/user-memory.md`
   - Project contexts: `./.co-improvement/learnt/contexts/**/*.json` (read all; drop malformed)
   - Project rubric index: `./.co-improvement/learnt/rubrics/index.json` (if present)
3. Persist draft artifacts (including the Intent list) before detailed review.
4. No state transition without explicit human checkpoint token.
5. For score overrides, require human reason for each changed score.
6. Never ask user to write files manually.
7. Always produce write-ready JSON memory updates for both context and rubric branches.
8. Reflection remains human-authored. AI scaffolds reflection and pressure-tests it, but does not replace it.
9. Every time AI proposes a suggestion, it must provide 2–3 feasible options, include side-effects/tradeoffs/risks for each, present key differences first in contrastive form, and ask human to decide by adding missing context or rubrics for future extension.
10. The adapted workflow draft must explicitly contain its own co-improvement lifecycle with alignment, draft/work, co-review, persistence, and reflection gates.
11. When Local Skill Output Mode applies, the final deliverable must be a valid local skill folder, not only a Markdown workflow draft.

## Mandatory Lifecycle (State Machine)

### Iteration Envelope
- For each draft section, run State 2 → State 3 → State 4 in order.
- Keep the loop on the current section until `REFLECT_OK`.
- Advance to the next section only after `REFLECT_OK`.

### State 0 — Alignment Gate (Human Required)
- Extract task objective, constraints, and deliverable type.
- Decide output mode: `local-skill` or `draft-workflow-only`.
- For `local-skill`, identify skill name, target path, trigger description, reusable resources, and which `.co-improvement/learnt` context/rubric memories should be referenced or bundled.
- Ask human alignment checkpoint token: `ALIGNMENT_OK`.
- Transition to State 1 only after `ALIGNMENT_OK`.

### State 1 — Draft Gate
- Build full draft using `references/meta-method.md`.
- If output mode is `local-skill`, also use `references/local-skill-output.md` and draft the target skill structure:
  - `SKILL.md` frontmatter and core workflow
  - optional `references/` files for bulky procedure details
  - optional `scripts/` only for deterministic checks or repeated fragile operations
  - `agents/openai.yaml` interface metadata when appropriate
- Keep `Intent` as a short intention list (2–5 bullets) near the top of the draft.
- Include a `Loop Scope Mapping` section that distinguishes:
  - how this skill's current meta-adaptation loop is being used to improve the adaptation work
  - how the resulting adapted workflow embeds its own co-improvement loop for future task execution
- Persist draft to:
  - Directory: `./.co-improvement/drafts/`
  - File: `<YYYYMMDD-HHMM>-<task-slug>.md`
- Confirm artifact path and ask human draft checkpoint token: `DRAFT_OK`.
- For `draft-workflow-only`, transition to State 2 only after `DRAFT_OK`.
- For `local-skill`, transition to State 1.5 only after `DRAFT_OK`.

### State 1.5 — Materialize Local Skill Gate
- Resolve helper scripts from installed skill directories:
  - `<skill_creator_skill_dir>/scripts/init_skill.py`
  - `<skill_creator_skill_dir>/scripts/quick_validate.py`
  - `<co_improvement_adapt_skill_dir>/scripts/bootstrap_memory_artifacts.sh`
- For a new local skill, run `<skill_creator_skill_dir>/scripts/init_skill.py <skill-name> --path <target-parent> --resources references` when practical.
- For an existing local skill, patch the existing target folder directly.
- The adapter must create or update the target local skill folder identified in State 0.
- The adapter must write the generated `SKILL.md`, plus any needed `references/`, `scripts/`, and `agents/openai.yaml` files.
- In practice, do not assume the target repository has its own `scripts/` folder; helper scripts come from the installed skill directories above.
- Run `<skill_creator_skill_dir>/scripts/quick_validate.py <skill-folder>` and record the result, or record why validation could not run.
- Confirm local skill path and materialization result.
- Transition to State 2 only after the local skill folder exists and validation has passed or the validation blocker is explicitly recorded.

Loop through State 2-4 for each section to improve the draft and human/AI ability:
### State 2 — Section Co-Review Gate
1. Print section title and content.
2. Check whether the section preserves both loop scopes: current meta-adaptation improvement and embedded future workflow improvement.
3. For any AI suggestion, provide 2–3 feasible options.
4. For each option, include expected side-effects, tradeoffs, and risk notes.
5. Present options in a contrastive format that highlights key differences first (what changes, what it costs, what risk it adds).
6. Ask human to decide by adding missing context or rubrics for future extension.
7. Propose AI scores for all 6 dimensions from `references/rubric.md` (1–5 each).
8. Provide one-line evidence for each proposed score.
9. Ask human to confirm or override each score.
10. If human overrides any score, require reason for each changed score.
11. Record changed scores and reasons in `Human Score Rationale Log`.
12. Compute final section total (`/30`) and status using human-approved scores.
13. If human confirms the draft, write the latest refined version to the corresponding file in `./.co-improvement/drafts/`.
14. Ask human co-review checkpoint token: `REVIEW_OK`.
15. Transition to State 3 only after `REVIEW_OK`.

### State 3 — Persist Learnings Gate
- Summarize quality patterns from section co-review outputs.
- For new co-improvement workflows, bootstrap memory artifacts with `<co_improvement_adapt_skill_dir>/scripts/bootstrap_memory_artifacts.sh ./.co-improvement/skills/memory-persistent`.
- Store patterns into `./.co-improvement/learnt/` according to `./.co-improvement/skills/memory-persistent/memory-protocol.md`.
- If output mode is `local-skill`, update the local skill artifact so the persisted skill can read or regenerate the relevant context/rubric memory in future runs.
- Ask human persistence checkpoint token: `PERSIST_OK`.
- Transition to State 4 only after `PERSIST_OK`.

### State 4 — Reflection Gate (Human Improvement)
- Run cognitive budget estimation using `references/cognitive-budget-estimation.md`.
- Run reflection flow using `references/reflection-paradigm.md`.
- Require final reflection answers in human-authored form.
- Ask human reflection checkpoint token: `REFLECT_OK`.
- Return to State 2 for the next section after `REFLECT_OK`; complete workflow after all sections are done.

## Completion Criteria
The final deliverable is the persisted adapted workflow or local skill, not a long transcript. When Local Skill Output Mode applies, the local skill folder is the primary deliverable and the `.co-improvement/drafts/` artifact is supporting evidence.

A run is complete only after a semantic check confirms that:
1. The persisted artifact can actually guide a future human-AI co-improvement run for the target task.
2. The artifact preserves both loop scopes: the current meta-adaptation loop and the embedded future workflow loop.
3. The artifact gives enough operational guidance for alignment, collaborative work, review, learning persistence, reflection, and future reuse without relying on unstated assumptions.
4. Useful context and rubric learnings were appended, merged, or explicitly skipped with reasons.
5. Required human checkpoint tokens were received for every completed state transition.
6. Rubric memory validation was run after rubric writes.
7. If a local skill was produced, `<skill_creator_skill_dir>/scripts/quick_validate.py <skill-folder>` passed, or the final handoff states why validation could not run.

The final chat response should be a compact handoff with the adapted workflow path, local skill path if created, memory paths created or changed, validation evidence, key human decisions, and unresolved risks.

## Progressive Disclosure References
- `references/meta-method.md`
- `references/rubric.md`
- `references/rubric-persistence-rubric.md`
- `references/context-persistence-rubric.md`
- `references/memory-protocol.md`
- `references/local-skill-output.md`
- `references/rubric-entry-template.md`
- `references/cognitive-budget-estimation.md`
- `references/reflection-paradigm.md`
- `./.co-improvement/learnt/contexts/`
- `./.co-improvement/learnt/rubrics/index.json`
