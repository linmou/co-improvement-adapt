# Reflection Paradigm (Post-Persistence Human Improvement)

## Purpose
Reflection improves both sides of the loop:
- Human mental model of AI strengths/limits in this task context.
- AI understanding of which human inputs (rubrics, constraints, examples, feedback) are actually useful.

This stage is not a score recap. It is a calibration step for the next loop.

## Inputs Required
- State 2 artifacts: section scores, overrides, reasons.
- State 3 artifacts: accepted memory items and skipped items.
- Cognitive budget estimate from `cognitive-budget-estimation.md`.

## Procedure
1. Select scaffold depth from budget estimate (`low`, `medium`, `high`).
2. Run the matching prompt set below.
3. Allow short AI-human discussion for clarification only.
4. Require final reflection answers to be human-authored.
5. Convert validated outputs into concise next-loop commitments.

## Prompt Sets by Scaffold Depth

### Low Budget (minimal but mandatory)
Use 3 prompts only:
1. "In this loop, AI helped most with: ___."
2. "In this loop, AI was weak or risky at: ___."
3. "One concrete change for next loop: ___."

Constraint:
- Each answer must be one sentence with one concrete example.

### Medium Budget (balanced)
Use 5 prompts:
1. "What did AI do well here, and what evidence supports that?"
2. "What did AI do poorly, and what failure mode was visible?"
3. "Which human inputs were useful (rubric/context/examples), and why?"
4. "Which human inputs were low-value/noisy, and why?"
5. "What two adjustments should we apply in the next loop?"

Constraint:
- At least one adjustment must change human behavior, not only AI instructions.

### High Budget (deep calibration)
Use 7 prompts:
1. "What AI capability mattered most in this task class?"
2. "What AI limitation mattered most in this task class?"
3. "Which rubric signals improved output quality the most?"
4. "Which constraints reduced quality or speed?"
5. "What did you initially assume that turned out wrong?"
6. "What should AI ask earlier next time?"
7. "Define a small experiment for the next loop and success criteria."

Constraint:
- Include one falsifiable experiment and one explicit stop condition.

## Anti-Offloading Guardrails
- AI can propose candidate phrasing, but final text must be rewritten or explicitly confirmed by human.
- Reject generic answers with no evidence ("it was helpful" without examples).
- Require at least one first-person statement from human ("I should...", "I over-constrained...").
- Require at least one change on human side and one change on AI side for next loop.

## Output Schema
1. `AI Strengths (Task-Scoped)`
2. `AI Limits (Task-Scoped)`
3. `Helpful Human Inputs`
4. `Unhelpful Human Inputs`
5. `Next-Loop Commitments`
6. `Open Question`

## Completion Condition
- Reflection checkpoint token `REFLECT_OK` is present.
- Answers satisfy scaffold constraints and anti-offloading guardrails.
