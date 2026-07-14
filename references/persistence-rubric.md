# Persistence Quality Rubric (Schema-Agnostic)

Use this rubric for any candidate memory item before appending.

Scale:
- 1 = poor / missing
- 2-3 = partial / weak
- 4 = good
- 5 = excellent

Dimensions (score all):
1. Non-Overlap
   - Adds genuinely new information versus existing memory.
2. Necessity
   - Likely to matter in future co-improvement loops.
3. Actionability
   - Enables concrete behavior change by agent or human.
4. Clarity
   - Concise, specific, and unambiguous.
5. Traceability
   - Backed by concrete evidence from section scores or human reasons.
6. Durability
   - Stable enough beyond one-off context.

Hard Gates:
- If `Non-Overlap < 4`: do not append as new item.
- Prefer `merge` over `append` when semantic duplication exists.

Decision Output Template:
- Candidate item: ...
- Scores:
  - Non-Overlap: [1-5]
  - Necessity: [1-5]
  - Actionability: [1-5]
  - Clarity: [1-5]
  - Traceability: [1-5]
  - Durability: [1-5]
- Decision: `append` | `merge` | `skip`
- Reason: ...
- Merge target (if merge): ...
