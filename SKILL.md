---
name: co-improvement-adapt
description: Use when a task must be adapted into a reusable human-AI co-improvement workflow or local Codex skill, with mandatory draft persistence, human checkpoints, rubric scoring, event-driven memory persistence, anytime reflection, and fallback closeout gates. Use when the user asks to turn .co-improvement results, project learnings, review workflows, or repeated human-in-the-loop procedures into a reusable workflow or skill.
---

# Human-AI Co-Improvement Task Adapter

## Core Principle
Run one mandatory human-in-the-loop pipeline in the same dialogue: align, draft, co-review, persist learnings, reflect. Persistence and reflection are event-driven first, with fallback closeouts so nothing is silently skipped.

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
4. No section-advance or irreversible gate close without explicit human checkpoint token. Event-driven persist/reflect interrupts resume the prior state and do not count as section advance. Memory **writes** are owned only by `$persist-rubrics-context` via its call contract; this host is a thin client (Request → Response) and never inlines JSON memory writes.
5. For score overrides, require human reason for each changed score.
6. Never ask user to write files manually.
7. After a learn interrupt or State 3 subagent call, host only requires: **subagent returned a Response** and (if present) **session Learning Log merged** from `learning_log_row`. Do not invent row schemas or require both memory branches.
8. Reflection remains human-authored. AI scaffolds reflection and pressure-tests it, but does not replace it.
9. Every time AI proposes a suggestion, it must provide 2–3 feasible options, include side-effects/tradeoffs/risks for each, present key differences first in contrastive form, and ask human to decide by adding missing context or rubrics for future extension.
10. The adapted workflow draft must explicitly contain its own co-improvement lifecycle with alignment, draft/work, co-review, event-driven persistence, anytime reflection, and fallback closeout gates.
11. When Local Skill Output Mode applies, the final deliverable must be a valid local skill folder, not only a Markdown workflow draft.
12. On human feedback that contains rubrics, contexts, reusable constraints, or generalizable score reasons, immediately spawn a **subagent** that runs `$persist-rubrics-context` using the client adapter in `references/persist-learnings-skill.md` and the callee contract `persist-rubrics-context/references/call-contract.md`; do not wait for section end.
13. On an **explicit** human request to reflect, or human text labeled as reflection / clearly answering reflection scaffold prompts, run the reflection flow immediately; do not wait for State 4 fallback. Ordinary co-review critique is not a reflection trigger.

## Mandatory Lifecycle (State Machine)

### Iteration Envelope (event-driven + fallback, not a rigid 2→3→4 pipeline)
- Keep the section open in State 2 until `REVIEW_OK`.
- During State 2 (and any non-terminal state), fire interrupts:
  - **Learn event** → subagent(`$persist-rubrics-context`) → resume prior state
  - **Reflect event** → run reflection flow → resume prior state
- Nested interrupts are allowed during State 3/4 fallback; they append Learning/Reflection Log rows and resume the interrupted closeout state. Only State 4 fallback may collect `REFLECT_OK`.
- After `REVIEW_OK`, run **fallback closeouts** only:
  1. State 3 fallback — human reviews learnings already decided / still pending
  2. State 4 fallback — show reflection already captured this loop, then formally close reflection
- Advance to the next section only after `PERSIST_OK` and `REFLECT_OK`.
- Do not re-run a full persist or full reflection pass when the interrupt path already covered the section; fallback is review + gap-fill. Resolve every Learning Log `pending` row before `PERSIST_OK`.

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
  - memory bootstrap (optional, when generating skills that need learnt helpers): `<persist_rubrics_context_skill_dir>/scripts/bootstrap_memory_artifacts.sh`
- For a new local skill, run `<skill_creator_skill_dir>/scripts/init_skill.py <skill-name> --path <target-parent> --resources references` when practical.
- For an existing local skill, patch the existing target folder directly.
- The adapter must create or update the target local skill folder identified in State 0.
- The adapter must write the generated `SKILL.md`, plus any needed `references/`, `scripts/`, and `agents/openai.yaml` files.
- In practice, do not assume the target repository has its own `scripts/` folder; helper scripts come from the installed skill directories above.
- Run `<skill_creator_skill_dir>/scripts/quick_validate.py <skill-folder>` and record the result, or record why validation could not run.
- Confirm local skill path and materialization result.
- Transition to State 2 only after the local skill folder exists and validation has passed or the validation blocker is explicitly recorded.

Loop each section with State 2 as the open work state; use event-driven skills for learning/reflection; use State 3/4 only as fallback closeouts.

### State 2 — Section Co-Review Gate (open work state)

#### Continuous interrupts while in State 2
These fire at any moment during State 2 (options discussion, scoring, overrides, free chat), not only at a fixed step:
- **Learn interrupt:** when the human provides rubrics, contexts, reusable constraints, generalizable score reasons, or an explicit save request:
  1. Build a **Request** per `references/persist-learnings-skill.md` (default `output_profile: standard`, `caller_tag: learn-interrupt`, `decision_mode: interactive`).
  2. Spawn a **subagent** whose sole task is `$persist-rubrics-context` with that Request (do not re-implement write logic).
  3. Subagent follows callee `SKILL.md` + `call-contract.md` and returns a versioned **Response** JSON.
  4. Merge `learning_log_row` (if included) into the session Learning Log; record writes/validation for later audit.
  5. **Resume State 2** (no section advance).
- **Reflect interrupt:** when the human **explicitly** asks to reflect, or sends text labeled as reflection / clearly answering scaffold prompts, run `references/reflection-paradigm.md`. If budget is unknown, default scaffold to `low` unless the human asks for deeper reflection; if a budget was already estimated this loop, reuse it. Append to the Reflection Log, then resume this state. Ordinary co-review comments are Learning Log or score-rationale material, not reflection.

#### Co-review sequence
1. Print section title and content.
2. Check whether the section preserves both loop scopes: current meta-adaptation improvement and embedded future workflow improvement.
3. For any AI suggestion, provide 2–3 feasible options.
4. For each option, include expected side-effects, tradeoffs, and risk notes.
5. Present options in a contrastive format that highlights key differences first (what changes, what it costs, what risk it adds).
6. Ask human to decide by adding missing context or rubrics for future extension.
7. Propose AI scores for all 6 dimensions from `references/rubric.md` (1–5 each).
8. Provide one-line evidence for each proposed score.
9. Ask human to confirm or override each score.
10. If human overrides any score, require reason for each changed score; if the reason is reusable, fire the learn interrupt.
11. Record changed scores and reasons in `Human Score Rationale Log`.
12. Compute final section total (`/30`) and status using human-approved scores.
13. If human confirms the draft, write the latest refined version to the corresponding file in `./.co-improvement/drafts/`.
14. Ask human co-review checkpoint token: `REVIEW_OK`.
15. After `REVIEW_OK`, enter fallback closeouts (State 3 fallback, then State 4 fallback). Do not treat State 3 as the only place learnings may be written.

### State 3 — Persist Learnings Fallback Gate (audit only; permanent host gate)
Write engine remains subagent(`$persist-rubrics-context`). This state is the permanent **audit gate**; it does not implement memory writes.
- Show the session Learning Log (merged Response `learning_log_row`s): decided and pending.
- For each pending row: build Request with `caller_tag: state3-pending-flush` (see adapter) and spawn subagent; merge Response before `PERSIST_OK`.
- Always run one **missed-candidate scan** against the Human Score Rationale Log and section discussion; spawn subagent with `caller_tag: state3-missed-scan` or record intentional skip.
- If the log is empty after the scan, say so and either capture last-minute learnings or record intentional empty persist.
- If a nested learn interrupt during State 4 creates new pending rows after `PERSIST_OK`, re-enter this audit gate before section advance (or force decide — no defer post-`PERSIST_OK`).
- If output mode is `local-skill`, confirm whether the skill still needs a memory-interface update.
- Ask `PERSIST_OK` only after no pending rows remain. Only this gate may collect `PERSIST_OK`.
- After `PERSIST_OK`, enter State 4 fallback.

### State 4 — Reflection Fallback Gate (Human Improvement)
Primary path is anytime reflection. This state is the **fallback closeout**.
- Show the session **Reflection Log**: reflection already captured/happened in this loop (if any).
- Run cognitive budget estimation using `references/cognitive-budget-estimation.md` if not already done for this loop; if reflecting lightly / budget still unknown, default scaffold `low` per `references/reflection-paradigm.md`.
- If reflection is incomplete for the selected scaffold depth, formally ask the remaining prompts from `references/reflection-paradigm.md`.
- If reflection already satisfies the scaffold and anti-offloading guardrails, present the captured answers for confirmation instead of re-interviewing from scratch.
- Require final reflection answers in human-authored form (or explicit human confirmation of captured text).
- Ask human reflection checkpoint token: `REFLECT_OK` (only this fallback may collect `REFLECT_OK`).
- Return to State 2 for the next section after `REFLECT_OK`; complete workflow after all sections are done.

## Completion Criteria
The final deliverable is the persisted adapted workflow or local skill, not a long transcript. When Local Skill Output Mode applies, the local skill folder is the primary deliverable and the `.co-improvement/drafts/` artifact is supporting evidence.

A run is complete only after a semantic check confirms that:
1. The persisted artifact can actually guide a future human-AI co-improvement run for the target task.
2. The artifact preserves both loop scopes: the current meta-adaptation loop and the embedded future workflow loop.
3. The artifact gives enough operational guidance for alignment, collaborative work, review, learning persistence, reflection, and future reuse without relying on unstated assumptions.
4. For each learn event: subagent returned a contract Response and session Learning Log was merged (or intentional empty/skip at State 3).
5. Required human checkpoint tokens were received for section advance and fallback closeouts (`REVIEW_OK`, `PERSIST_OK`, `REFLECT_OK`); event-driven interrupts left Learning/Reflection logs.
6. When Response included `validation` after rubric writes, it is present in the handoff (host does not re-implement validation).
7. If a local skill was produced, `<skill_creator_skill_dir>/scripts/quick_validate.py <skill-folder>` passed, or the final handoff states why validation could not run.
8. Persistence used subagent(`$persist-rubrics-context`) via call-contract; State 3 audited session rows rather than writing memory inline.
9. Reflection could run anytime; State 4 fallback showed reflection that already happened in the loop and formally closed gaps.

The final chat response should be a compact handoff with the adapted workflow path, local skill path if created, memory paths created or changed, validation evidence, key human decisions, and unresolved risks.

## Progressive Disclosure References
- `references/meta-method.md`
- `references/rubric.md` (section scoring dimensions for co-review — not learnt memory)
- `references/persist-learnings-skill.md` (thin client adapter: Request builders + Response merge)
- `${CODEX_HOME:-$HOME/.codex}/skills/persist-rubrics-context/SKILL.md` (write engine)
- `${CODEX_HOME:-$HOME/.codex}/skills/persist-rubrics-context/references/call-contract.md` (Request/Response SoT)
- `${CODEX_HOME:-$HOME/.codex}/skills/persist-rubrics-context/references/memory-protocol.md` (storage execution only)
- `references/local-skill-output.md`
- `references/cognitive-budget-estimation.md`
- `references/reflection-paradigm.md`
- `./.co-improvement/learnt/contexts/` (read path)
- `./.co-improvement/learnt/rubrics/index.json` (read path)
