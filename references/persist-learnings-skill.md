# Persist client adapter (one-way import)

This host **imports** `$persist-rubrics-context` like a submodule.  
It does not own write mechanics or redefine Response schemas.

**Contract SoT (callee):**  
`${CODEX_HOME:-$HOME/.codex}/skills/persist-rubrics-context/references/call-contract.md`

**Skill entry (callee):**  
`${CODEX_HOME:-$HOME/.codex}/skills/persist-rubrics-context/SKILL.md`

```
host event → build Request → subagent($persist-rubrics-context) → Response → merge session log → resume host
```

## Host owns
1. **Read** project memory at run start (SKILL.md rule 2).
2. **When** to call (learn interrupt, State 3 pending flush, missed-candidate scan).
3. **Request** construction (below); default `output_profile: standard`.
4. **Merge** Response `learning_log_row` (if present) into the session Learning Log list.
5. Host tokens only: `PERSIST_OK` at State 3 audit (never issued by the write skill).

## Host does not
- Inline learnt JSON writes
- Ship or copy memory-protocol / validators
- Invent Learning Log field schemas (use Response as-is)

## Request builders

All optional fields use callee defaults if omitted. Prefer explicit fields for clarity.

### Learn interrupt (`caller_tag: learn-interrupt`)
```json
{
  "project_root": "<cwd project root>",
  "human_feedback": "<verbatim human feedback>",
  "section_id": "<current section id or null>",
  "caller_tag": "learn-interrupt",
  "decision_mode": "interactive",
  "output_profile": "standard"
}
```

### State 3 pending flush (`caller_tag: state3-pending-flush`)
Same shape; `human_feedback` restates the pending candidate. Use `decision_mode: predecided` + `pre_decision` if the human already chose at audit time; otherwise `interactive`.

### State 3 missed-candidate scan (`caller_tag: state3-missed-scan`)
Same shape; `human_feedback` is the missed reusable material (or explicit skip rationale). `propose_only` is allowed if the host only wants proposals before a later flush.

`caller_tag` is **opaque** to the write skill — for host logs only. Do not expect the write skill to understand host state names.

## Response merge
1. Require subagent completion with Response `version: 1` JSON (see call-contract).
2. If `include` / profile returned `learning_log_row`, append it to the session Learning Log (host-owned list).
3. Record `status`, `writes`, `validation` for State 3 display.
4. Resume prior host state; do not advance the section envelope from the subagent.

## Assets used only inside the subagent
Paths under `${CODEX_HOME:-$HOME/.codex}/skills/persist-rubrics-context/` only — not under this skill.
