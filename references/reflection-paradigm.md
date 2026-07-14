# Reflection Paradigm (Anytime + Fallback Closeout)

## Purpose
Reflection improves both sides of the loop:
- Human mental model of AI strengths/limits in this task context.
- AI understanding of which human inputs (rubrics, constraints, examples, feedback) are actually useful.

This stage is not a score recap. It is a calibration step for the next loop.

## Trigger modes
1. **Anytime (primary):** run immediately when the human **explicitly** asks to reflect, labels text as reflection, or clearly answers reflection scaffold prompts mid-loop. Do not wait for section end or State 4 fallback.
2. **Fallback closeout:** after `REVIEW_OK` and `PERSIST_OK`, show reflection already captured/happened in this loop, fill remaining scaffold gaps, and formally ask for `REFLECT_OK`.

Non-triggers (treat as co-review or Learning Log material unless the human opts into reflection):
- Ordinary evaluative comments during scoring ("AI was weak on X")
- Preference or wording nits not framed as loop calibration
- Score override reasons (those go to the learn interrupt if reusable)

Both modes append to the session **Reflection Log**. Fallback must not re-interview from scratch when the log already satisfies the scaffold. Only State 4 fallback may collect `REFLECT_OK`.

## Inputs Required
- Available State 2 artifacts: section scores, overrides, reasons (may be partial if reflecting early).
- Learning Log / State 3 artifacts when present: accepted memory items and skipped items.
- Cognitive budget estimate from `cognitive-budget-estimation.md`.

## Procedure
1. If a budget was already estimated this loop, reuse it. Otherwise run `cognitive-budget-estimation.md` only when the human wants medium/high depth or when running fallback closeout.
2. If anytime mode and budget is unknown, default scaffold to `low` unless the human asks for deeper reflection.
3. Select scaffold depth (`low`, `medium`, `high`) from the budget estimate or the default above.
4. Run the matching prompt set below (or only the unanswered prompts when resuming from the Reflection Log).
5. Allow short AI-human discussion for clarification only.
6. Require final reflection answers to be human-authored.
7. Convert validated outputs into concise next-loop commitments.
8. Write or update the Reflection Log row for this loop (timestamp, mode=`anytime|fallback`, answers, still-open prompts).

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
- For anytime interrupts: Reflection Log updated; prior state resumed; `REFLECT_OK` is optional until section closeout.
- For fallback closeout: reflection checkpoint token `REFLECT_OK` is present.
- Answers satisfy scaffold constraints and anti-offloading guardrails (or gaps are explicitly deferred with human consent before `REFLECT_OK`).
