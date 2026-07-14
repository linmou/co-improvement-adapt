# Cognitive Budget Estimation (Evidence-Based)

## Purpose
Estimate the current human attention/cognitive budget for this loop so reflection depth matches reality.

This is a routing estimate, not a diagnosis.

## Evidence Window
Use recent interaction evidence only:
- Last 8–15 human turns in current thread.
- Recent interruption/redo events.
- Specificity and correction patterns in user feedback.

Do not infer from personality labels.

## Scoring Dimensions (1–5 each)

### 1) Continuity Stability
How stable the dialogue flow is.
- 1: Frequent interruptions, resets, or abandoned partial paths.
- 3: Some interruptions but thread continuity mostly preserved.
- 5: Stable turn-taking with coherent progress.

### 2) Instruction Specificity
How concrete and testable user requests are.
- 1: Vague or shifting requests without anchors.
- 3: Mixed specificity.
- 5: Clear constraints, targeted corrections, explicit outcomes.

### 3) Correction Precision
How actionable user corrections are.
- 1: Broad dissatisfaction only.
- 3: Partial actionable edits.
- 5: Direct pinpoint corrections with intent.

### 4) Meta-Reasoning Engagement
How much the user engages in why/how framing.
- 1: Only output-level edits.
- 3: Occasional rationale discussion.
- 5: Frequent discussion of assumptions, tradeoffs, and process.

### 5) Iteration Stamina
How sustained the user is across multiple refinement cycles.
- 1: Drops quickly after one revision.
- 3: Moderate willingness to iterate.
- 5: Sustains multi-round refinement with coherence.

## Compute Budget Band
- Total score range: 5–25.
- `Low` budget: 5–11 → use low scaffold.
- `Medium` budget: 12–18 → use medium scaffold.
- `High` budget: 19–25 → use high scaffold.

If evidence is mixed, pick the lower band and keep reflection lightweight.

## Cognitive Risk Flags
Check and report if present:
- `context-thrash`: frequent direction changes with incomplete closure.
- `premature-closure`: tendency to accept before key checks complete.
- `over-constraint-drift`: constraints added faster than validated impact.

## Output Format
- `Budget Band`: low|medium|high
- `Dimension Scores`: [stability, specificity, correction, meta, stamina]
- `Evidence`: 3 short bullets from recent turns
- `Risk Flags`: optional list
- `Chosen Reflection Scaffold`: low|medium|high

## Guardrail
Never use budget estimation to skip reflection. Use it only to choose reflection depth.
