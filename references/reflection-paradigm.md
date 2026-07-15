# Reflection (host pointer)

Reflection is implemented by the independent skill **`$reflect-user-memory`**.

- Skill: `${CODEX_HOME:-$HOME/.codex}/skills/reflect-user-memory/SKILL.md`
- Contract: `.../reflect-user-memory/references/call-contract.md`
- User-memory structure: `.../reflect-user-memory/references/user-memory-structure.md`
- Host adapter: `references/reflect-client-adapter.md`

## Host behavior (summary)
1. On reflect interrupt or State 4 fallback, build Request and spawn **subagent(`$reflect-user-memory`)**.
2. Merge Response `reflection_log_row` into the session Reflection Log.
3. Durable L1 storage is **`~/.codex/user-memory.md`** (digest + optional standing promotions) — owned by the reflect skill.
4. Only State 4 fallback collects **`REFLECT_OK`**.

Do not reimplement reflection prompts or user-memory writes in this host.
