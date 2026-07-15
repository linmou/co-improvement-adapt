# Reflect client adapter (one-way import)

Host imports `$reflect-user-memory` for structured reflection + L1 digest.  
Does not own user-memory schema or prompt sets.

**Contract SoT:**  
`${CODEX_HOME:-$HOME/.codex}/skills/reflect-user-memory/references/call-contract.md`

**Skill:**  
`${CODEX_HOME:-$HOME/.codex}/skills/reflect-user-memory/SKILL.md`

```
host reflect event → Request → subagent($reflect-user-memory) → Response → merge session Reflection Log → resume
```

## Host owns
1. When to call (reflect interrupt; State 4 fallback).
2. Packing `loop_context` (section scores, Learning Log highlights, task slug).
3. Merging `reflection_log_row` into session Reflection Log.
4. Host token **`REFLECT_OK`** only at State 4 fallback.

## Host does not
- Rewrite `~/.codex/user-memory.md` structure
- Inline full reflection prompt procedure
- Persist project learnt from reflection (use `$persist-rubrics-context` if project fact)

## Request builders

### Reflect interrupt (`caller_tag: reflect-interrupt`)
```json
{
  "loop_context": "<section + scores + learning highlights>",
  "scaffold": "auto",
  "decision_mode": "interactive",
  "persist": true,
  "promote_standing": "ask",
  "caller_tag": "reflect-interrupt",
  "section_id": "<current section or null>"
}
```

### State 4 fallback (`caller_tag: state4-fallback`)
Same shape; pass any existing session reflection answers in `human_reflection` if already captured. Set `scaffold` from cognitive budget if known. Host collects `REFLECT_OK` after successful Response (`status=completed` or deferred gaps with human consent).

## Response merge
1. Append `reflection_log_row` to session Reflection Log.
2. Surface `user_memory.path` and whether digest was appended.
3. Resume prior host state; only State 4 may ask for `REFLECT_OK`.
