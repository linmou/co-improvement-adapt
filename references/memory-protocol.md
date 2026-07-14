# Memory Protocol (JSON-First: Context + Rubric)

Purpose: define where project memory lives, how it is written, how memory is retrieved, and how human feedback updates both context and rubric memory.

## Scope
- Context root: `./.co-improvement/learnt/contexts/`
- Context entries: `./.co-improvement/learnt/contexts/<domain>/<context-id>.json`
- Rubric root: `./.co-improvement/learnt/rubrics/`
- Rubric index: `./.co-improvement/learnt/rubrics/index.json`
- Rubric entries: `./.co-improvement/learnt/rubrics/<domain>/<rubric-id>.json`
- Rubric add/update decision source: `references/rubric-persistence-rubric.md`
- Context add/update decision source: `references/context-persistence-rubric.md`
- Consistency checker: `scripts/validate_rubric_memory.py`

## 1) Context Memory Branch (No Index)
### Storage
1. Store context as JSON files under `./.co-improvement/learnt/contexts/`.
2. Do not create `contexts/index.json`.
3. Keep one context entry per file.
4. Context memory is project-wide and should be considered as a whole.

### Write
1. Build candidate contexts from section review rationale and human feedback.
2. Evaluate candidate with `references/context-persistence-rubric.md` and decide `append | merge | skip`.
3. Decide `append | merge | skip`:
   - `append`: create one new context file.
   - `merge`: update an existing context file when it is the same core context.
   - `skip`: do not write.
4. If `append` vs `merge` is ambiguous, ask human before writing.
5. Keep wording concrete and reusable across future loops.

### Retrieve (Initial Version)
1. Read all JSON files under `./.co-improvement/learnt/contexts/` recursively.
2. Drop malformed files.
3. Return all valid contexts (no index and no keyword filtering in initial version).

## 2) Rubric Memory Branch (Indexed)
### Storage
1. Use `index.json` as router and rubric JSON files as source of truth.
2. Store full rubric content only in rubric entry files, not in `index.json`.
3. Keep one rubric entry per file.
4. `id` must be unique across active rows in `index.json`.
5. Keep `index.json` minimal fields only:
   - `id`
   - `path`
   - `status` (`active` or `deprecated`)
   - `intent_keywords`
   - `context_keywords`
   - `applicability_summary`
6. Do not use `priority`.
7. Do not use `version` in `index.json`; index routes to latest maintained active entry.
8. Do not use `supersedes` in `index.json`.

### Write
1. Build candidate rubrics from section review rationale.
2. Normalize candidate to rubric JSON schema.
3. Evaluate candidate with `rubric-persistence-rubric.md` and decide `append | merge | skip`.
4. If `append` and `merge` are both plausible, ask human to choose before writing.
5. Execute write in one change set:
   - `append`:
     - create one new rubric JSON file under `rubrics/<domain>/`
     - add one `active` object to `index.json`
   - `merge`:
     - update refined rubric JSON file as latest for existing rubric `id`
     - update matching `index.json` object fields (`path`, keywords, applicability summary) if needed
     - keep exactly one `active` object per `id`
   - `skip`:
     - do not write
6. Reject malformed candidates.
7. Run consistency check after each write:
   - `python3 ~/.codex/skills/co-improvement-adapt/scripts/validate_rubric_memory.py --project-root <project_root>`

### Retrieve
Input:
- current intent list
- current context snapshot
- all project contexts from Context Memory Branch

Steps:
1. Load `index.json` first.
2. Keep objects where `status = active`.
3. Enforce latest-only invariant:
   - for each `id`, keep exactly one active object.
4. Apply coarse prefilter using `intent_keywords` and `context_keywords`.
5. Load only filtered rubric files by `path`.
6. Drop malformed entries or missing-file rows.
7. Apply semantic filters from rubric content:
   - `applicability.include` / `applicability.exclude`
   - `dependencies.context_refs` / `dependencies.intent_refs`
8. Return selected rubrics with one-line selection reason each.

## 3) Usage Output + Human Feedback Protocol
For each loop, print and collect:
1. Context set used:
   - context file paths
   - short summary of each loaded context
2. Rubric set selected:
   - `id`, `title`, `path`, selection reason
3. AI scoring result:
   - score values by rubric slots
   - short reason for each score
4. Human review result:
   - confirmed or overridden score
   - reason for each override
5. Feedback log for updates:
   - mismatch patterns
   - proposed context updates (`append | merge | skip`)
   - proposed rubric updates (`append | merge | skip`)

## Validation Checklist (Before Write)
- Context files are valid JSON and include required keys.
- `index.json` active `id` values are unique.
- `index.json` `path` values are valid and existing.
- `index.json` contains no `priority` key.
- `index.json` contains no `version` key.
- `index.json` contains no `supersedes` key.
- Rubric file has required keys: `id`, `title`, `applicability`, `decision_rule`, `dependencies`, `lifecycle`.
- `applicability.include` and `applicability.exclude` are non-empty lists.
- `dependencies.context_refs` and `dependencies.intent_refs` are non-empty lists.
- For each score level used:
  - `score_X_rule` exists
  - `score_X_support_examples` is a non-empty list
  - `score_X_counter_examples` is a list of `[counter+, counter-]` pairs

## Context Entry JSON Minimal Template
```json
{
    "id": "CTX-TEAM-FATIGUE-RISK",
    "statement": "Long multi-step tasks increase fatigue risk and reduce human review quality.",
    "intent_keywords": ["decomposition", "review quality"],
    "context_keywords": ["long task", "fatigue"],
    "scope": {
        "include": ["multi-step tasks"],
        "exclude": ["single-step quick edits"]
    },
    "lifecycle": {
        "sunset_condition": ""
    }
}
```

## `index.json` Minimal Template (Rubrics)
```json
[
    {
        "id": "RUB-TASK-DECOMPOSITION",
        "path": "./.co-improvement/learnt/rubrics/workflow/rub-task-decomposition.json",
        "status": "active",
        "intent_keywords": ["task split", "role mapping"],
        "context_keywords": ["long task", "fatigue risk"],
        "applicability_summary": "use for multi-step workflows; exclude one-shot tasks"
    }
]
```

## Notes
- JSON is single source of truth; AI can render readable summaries for HITL review.
- Context branch is intentionally index-free in initial version; retrieval reads all contexts.
- Use `context-persistence-rubric.md` as authority for context `append | merge | skip`.
- Do not duplicate rubric decision logic here; use `rubric-persistence-rubric.md` as authority for rubric `append | merge | skip`.
- Use `rubric-entry-template.md` as the only rubric entry schema source.
- If index metadata conflicts with rubric file content, trust rubric file content and repair index.
