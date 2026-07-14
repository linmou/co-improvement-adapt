# Rubric Persistence Rubric (Add/Update for `rubrics.md`)

Use this rubric before adding or updating rubric entries in project memory.

## Scope
- Target memory: project `rubrics.md`
- Entry shape: `rubric-entry-template.md`
- Operation type: `add` or `update`

## Scale
- 1 = poor / missing
- 2-3 = partial / weak
- 4 = good
- 5 = excellent

## Dimensions (score all)
1. Non-Overlap
   - `add`: genuinely new versus existing entries.
   - `update`: materially improves an existing entry without duplicating another.
2. Decision Rule Quality
   - Rules are explicit, testable, and map cleanly to score levels.
   - Support examples and counter example pairs are consistent with the rule.
3. Dependency Grounding
   - `dependencies.context_refs` and `dependencies.intent_refs` clearly justify why this rubric should exist.
4. Applicability Clarity
   - `applicability.include` and `applicability.exclude` define valid boundaries without ambiguity.
5. Reuse Value
   - Entry is likely reusable across multiple future loops, not one-off.
6. Durability
   - Stable enough beyond transient phrasing or temporary workflow detail.

## Hard Gates (must pass)
1. Dependencies complete
   - `dependencies.context_refs` is non-empty
   - `dependencies.intent_refs` is non-empty
   - references are written in natural language
2. Applicability boundaries present
   - both `applicability.include` and `applicability.exclude` exist and are non-empty
3. Score structure complete
   - for each declared score level `X`, all exist:
     - `score_X_rule`
     - `score_X_support_examples` (non-empty list)
     - `score_X_counter_examples` (non-empty list)
4. Counter example pair format valid
   - each `score_X_counter_examples` item is a two-item list: `[counter+, counter-]`
   - `counter+` corresponds to one adjacent upper level only (`X+1`), unless top-level uses `N/A`
   - `counter-` corresponds to one adjacent lower level only (`X-1`), unless bottom-level uses `N/A`
   - each `[counter+, counter-]` pair contrasts one main feature only
5. Decision rule is testable
   - no vague principle-only wording
6. Non-overlap threshold for append
   - if `Non-Overlap < 4`, do not `append` as a new entry

## Decision Policy
- `append`: pass all hard gates, `Non-Overlap >= 4`, `Decision Rule Quality >= 4`, `Reuse Value >= 4`.
- `merge`: pass hard gates, but semantic overlap exists and candidate improves precision/examples of an existing entry.
- `skip`: fail any hard gate, or weak `Decision Rule Quality`/`Reuse Value`.
- `ask_human`: use when `append` and `merge` both look plausible (boundary overlap or unclear scope split).

## Decision Output Template
- Candidate rubric id/title: ...
- Operation type: `add` | `update`
- Scores:
  - Non-Overlap: [1-5]
  - Decision Rule Quality: [1-5]
  - Dependency Grounding: [1-5]
  - Applicability Clarity: [1-5]
  - Reuse Value: [1-5]
  - Durability: [1-5]
- Hard gate check:
  - Dependencies complete: [pass/fail]
  - Applicability boundaries present: [pass/fail]
  - Score structure complete: [pass/fail]
  - Counter example pair format valid: [pass/fail]
  - Decision rule is testable: [pass/fail]
  - Non-overlap threshold for append: [pass/fail]
- Decision: `append` | `merge` | `skip`
- Reason: ...
- Merge target (if merge): ...
