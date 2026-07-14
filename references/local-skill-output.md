# Local Skill Output

Use this reference when `co-improvement-adapt` turns an adapted workflow into a reusable local Codex skill.

## Output Decision

Create or update a local skill when any condition is true:

- The user asks for a skill or says the `.co-improvement/` results should become reusable.
- The workflow is expected to be invoked later with `$skill-name`.
- The workflow contains stable context, rubrics, state gates, or repeatable human-in-the-loop behavior.

Skip local skill creation only when the user explicitly wants a one-off draft or the workflow is not reusable.

## Target Location

Default to `${CODEX_HOME:-$HOME/.codex}/skills/<skill-name>` unless the user specifies another local path.

Resolve helper scripts from installed skill directories. In practice, do not assume the target repository has its own `scripts/` folder:

- `<skill_creator_skill_dir>/scripts/init_skill.py`
- `<skill_creator_skill_dir>/scripts/quick_validate.py`
- `<persist_rubrics_context_skill_dir>/scripts/bootstrap_memory_artifacts.sh` (memory helpers only; write engine is `$persist-rubrics-context`)

For a new skill, use the `skill-creator` initialization flow when practical:

```bash
<skill_creator_skill_dir>/scripts/init_skill.py <skill-name> --path "${CODEX_HOME:-$HOME/.codex}/skills" --resources references
```

For an existing skill, patch the existing files directly and validate afterward.

Materialize the skill folder before treating the workflow as delivered:

1. Create or update the target local skill folder.
2. Write the generated `SKILL.md`.
3. Write any required `references/`, optional deterministic `scripts/`, and optional `agents/openai.yaml`.
4. Run validation and record the result.

## Required Skill Shape

The generated skill must include:

1. `SKILL.md` with YAML frontmatter containing only `name` and `description`.
2. A concise body that tells future Codex runs exactly how to execute the workflow.
3. A required embedded co-improvement lifecycle:
   - alignment gate
   - draft/work gate
   - representative edit or work-sample gate when applicable
   - co-review gate (open work state with continuous learn/reflect interrupts)
   - event-driven persistence on human rubric/context feedback (pre-write human `append|merge|skip`), plus persistence fallback closeout with Learning Log review and `PERSIST_OK`
   - anytime reflection on explicit human request, plus reflection fallback closeout with Reflection Log review and `REFLECT_OK`
4. Explicit human checkpoint tokens or equivalent human-confirmation prompts (`ALIGNMENT_OK`, work/review tokens, `PERSIST_OK`, `REFLECT_OK` as applicable).
5. A "Human Improvement Space" section describing what the human can refine over time:
   - context
   - rubrics
   - examples
   - negative examples
   - scope boundaries
   - reflection depth
6. A "Memory Interface" section explaining: (a) how the skill **reads** project `.co-improvement/learnt` contexts and rubrics, and (b) that **writes** go only through subagent(`$persist-rubrics-context`) — do not re-implement memory-protocol/validators in the generated skill unless the human explicitly wants bundled helpers.
7. A "Validation" section naming deterministic checks, semantic checks, and manual review gates.

Keep bulky schemas, sample records, rubrics, and templates in `references/` instead of bloating `SKILL.md`.

## Human-In-The-Loop Improvement Space

Every local skill produced by this adapter must leave visible slots for future human improvement. Prefer concrete headings such as:

```markdown
## Human Improvement Space
- Add context when a human correction reveals a stable project fact; learn interrupt → subagent(`$persist-rubrics-context`) immediately; human chooses append|merge|skip before write; do not wait for section end.
- Add or refine rubrics when a correction changes how future outputs should be judged; same subagent(`$persist-rubrics-context`) path and Learning Log (`pending` until decided).
- Record representative edits before document-wide or workflow-wide propagation.
- Reflect at any time on an explicit reflect request; still run a fallback reflection closeout that shows the Reflection Log and collects `REFLECT_OK`.
- Keep reflection effort adjustable; default to the project preference when known (anytime default scaffold low if budget unknown).
```

Generated skills must operationalize the learn interrupt as subagent(`$persist-rubrics-context`) (or an equivalent subagent procedure), including Learning Log fields and host fallback `PERSIST_OK`.

Do not hide human improvement only in prose. Make it operational: future users must know where to add context, when to update rubrics, and when to stop propagation.

## Memory Packaging

Prefer referencing project memory by path when the skill is project-specific:

```markdown
Read `.co-improvement/learnt/contexts/**/*.json` and `.co-improvement/learnt/rubrics/index.json` before proposing edits.
```

Prefer bundling stable, project-agnostic templates inside the skill's `references/` folder when the skill should work across projects.

Do not copy volatile project facts into a global skill unless the user explicitly wants a project-specific skill.

## Validation Checklist

Before final handoff:

1. Run `quick_validate.py` on the skill folder:

```bash
<skill_creator_skill_dir>/scripts/quick_validate.py <skill-folder>
```

2. If rubric memory changed, rely on `$persist-rubrics-context` subagent validator output (do not re-implement validation in the adapter).
3. Check that the skill can be triggered from its frontmatter description.
4. Check that the embedded co-improvement loop is explicit and not merely implied.
5. Check that human checkpoint tokens or confirmation prompts exist before irreversible propagation, persistence fallback closeout, and reflection fallback closeout.
6. Check that event-driven persist and anytime reflection are specified, not only end-of-section gates.
7. Check that the final handoff names the local skill path and any unresolved risks.
