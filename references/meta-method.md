### Meta-Method Principles & Instructions (Reusable Design Patterns)

Overarching Principles (unchanged):
- Minimize human design effort: Templates + AI-drafting
- Maximize output standards & improvement: AI consistency + task complexity for implicit gains
- Framework Fidelity: Uniqueness, bidirectional facilitation, closed loops
- Meta-Output: Produce reusable workflow blueprints
- Two-Level Loop Fidelity: use the co-improvement loop during adaptation, and require the produced blueprint to embed its own co-improvement loop for future execution

1. Design for Task Decomposition
   - Principles: Modular → reveal leverage points; clarity > depth
   - Instructions: Aim 6–12 subtasks; classify each (AI-fit / human-fit / hybrid); include "unique human input" slots (personal context, intuition, long-term memory)
   - Template phrase for blueprint: "Subtask X: [description] – Classification: [AI/human/hybrid] – Human provides: [context slot if needed]"

2. Design for Uniqueness Mapping & Bidirectional Facilitation
   - Principles: Create tight support loops; focus human gains on task-specific abilities (domain judgment, pattern detection, salience, decision quality under constraints)
   - Human → AI facilitation patterns (choose 2–3 per adaptation):
     - Precise rubrics: scoring criteria (1–5 scales), success thresholds, prioritization rules (e.g., "Rank options first by long-term impact, then feasibility")
     - Constraint templates: "Must satisfy: ethical boundary A, budget limit B, brand voice C"
     - Context injection: "Incorporate this background only I know: [slot for human to fill]"
     - Steering statements: "When sampling, weight toward [X outcome] unless contradicted by evidence"
     - Results of Inductive reasoning: "Based on [some examples] I noticed that [findings]"
     - Final decision under ambiguity.
     - Mange resource devotion to each task. Balance between 'exploit' and 'exploration'.

   - AI → human facilitation patterns (choose 2–4 per adaptation):
     - Task-focused reflection prompts: 
       - "Which of these 3–5 patterns do you see most clearly here, and why?"
       - "What task-specific assumption are you making? Is the opposite plausible?"
       - "Rank these options by [your success criteria]; explain the top choice"
       - "Where do you see highest uncertainty / ambiguity in this subtask?"
     - Controlled sampling handoff: "Here are 12–20 generated variations — select top 3 and justify using task criteria"
     - Critique nudges: "Critique this draft against the rubric you provided earlier"
     - Decision-forcing questions: "Given the constraints, what one change would most improve outcome quality?"
     - Reduce ambiguity by continuous questioning.
     - Assist resource management among tasks. Remind if you have digged into one rabit hole too much.

   - Mapping format (use table in blueprint):
     | Uniqueness | Mapped to Subtask(s) | Facilitation Direction | Example Mechanism |
     |------------|----------------------|------------------------|-------------------|

3. Design for Closed-Loop Structure
   - Principles: Self-refining; task-ability gains via repeated judgment/solving; automation-heavy
   - Instructions:
     - Loop Scope Mapping: explicitly separate the meta-adaptation loop being run now from the embedded workflow loop that future users will run later
     - Initial Alignment: 1-turn template – Human: "My bandwidth/style/preferences"; AI: "My strengths/gaps in this domain"
     - Iterative Core (2–6 rounds):
       - Pattern A (high-AI-exposure): AI runs bulk sampling/analysis → outputs ranked list + evidence → human selects/refines via 1–2 prompts
       - Pattern B (low-AI-exposure): Human provides deeper context → AI generates options/counterfactuals → human judges salience/ethical fit
       - Feedback closure: "Incorporate this change → refine rubric X for next round"
     - Embedded Lifecycle: include alignment, draft/work, co-review, persistence, and reflection gates inside the adapted workflow blueprint
     - End/Transfer: Summary template + "Reuse refined rubric for similar task Y?"

4. Design for Wrap & Longitudinal Transfer
   - Principles: Build reusability habit
   - Instructions: Include 2-min reflection template: "Task ability most exercised? Transferable insight? Refined rubric worth saving?"
