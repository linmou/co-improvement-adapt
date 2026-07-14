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
- `<co_improvement_adapt_skill_dir>/scripts/bootstrap_memory_artifacts.sh`

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
   - co-review gate
   - persistence gate
   - reflection gate
4. Explicit human checkpoint tokens or equivalent human-confirmation prompts.
5. A "Human Improvement Space" section describing what the human can refine over time:
   - context
   - rubrics
   - examples
   - negative examples
   - scope boundaries
   - reflection depth
6. A "Memory Interface" section explaining how the skill reads, writes, or references project `.co-improvement/learnt` context and rubric memory.
7. A "Validation" section naming deterministic checks, semantic checks, and manual review gates.

Keep bulky schemas, sample records, rubrics, and templates in `references/` instead of bloating `SKILL.md`.

## Human-In-The-Loop Improvement Space

Every local skill produced by this adapter must leave visible slots for future human improvement. Prefer concrete headings such as:

```markdown
## Human Improvement Space
- Add context when a human correction reveals a stable project fact.
- Add or refine rubrics when a correction changes how future outputs should be judged.
- Record representative edits before document-wide or workflow-wide propagation.
- Keep reflection effort adjustable; default to the project preference when known.
```

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

2. If rubric memory changed, run the co-improvement rubric validator.
3. Check that the skill can be triggered from its frontmatter description.
4. Check that the embedded co-improvement loop is explicit and not merely implied.
5. Check that human checkpoint tokens or confirmation prompts exist before irreversible propagation, persistence, and reflection closure.
6. Check that the final handoff names the local skill path and any unresolved risks.
