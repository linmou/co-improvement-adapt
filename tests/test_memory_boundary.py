#!/usr/bin/env python3
# Tests that co-improvement-adapt is a memory host only: read + audit + subagent,
# with write engine owned solely by $persist-rubrics-context.

from pathlib import Path
import os
import unittest


ROOT = Path(__file__).resolve().parents[1]
SKILL_MD = ROOT / "SKILL.md"
PERSIST_POINTER = ROOT / "references" / "persist-learnings-skill.md"
LOCAL_SKILL_OUTPUT = ROOT / "references" / "local-skill-output.md"

# Write-engine assets must NOT live under adapt (single copy under persist).
PRUNED_PATHS = [
    ROOT / "references" / "memory-protocol.md",
    ROOT / "references" / "context-persistence-rubric.md",
    ROOT / "references" / "rubric-persistence-rubric.md",
    ROOT / "references" / "rubric-entry-template.md",
    ROOT / "references" / "persistence-rubric.md",
    ROOT / "references" / "memory-template.md",
    ROOT / "scripts" / "validate_rubric_memory.py",
    ROOT / "scripts" / "bootstrap_memory_artifacts.sh",
]


def codex_home() -> Path:
    env = os.environ.get("CODEX_HOME")
    if env:
        return Path(env)
    return Path.home() / ".codex"


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


class MemoryBoundaryTest(unittest.TestCase):
    def test_write_engine_assets_removed_from_adapt(self) -> None:
        for path in PRUNED_PATHS:
            self.assertFalse(
                path.is_file(),
                f"write-engine asset must not live in adapt: {path.relative_to(ROOT)}",
            )

    def test_persist_skill_holds_single_write_copy(self) -> None:
        skill_root = codex_home() / "skills" / "persist-rubrics-context"
        required = [
            skill_root / "SKILL.md",
            skill_root / "references" / "memory-protocol.md",
            skill_root / "references" / "context-persistence-rubric.md",
            skill_root / "references" / "rubric-persistence-rubric.md",
            skill_root / "references" / "rubric-entry-template.md",
            skill_root / "scripts" / "validate_rubric_memory.py",
            skill_root / "scripts" / "bootstrap_memory_artifacts.sh",
        ]
        for path in required:
            self.assertTrue(path.is_file(), f"missing persist write-engine asset: {path}")

    def test_adapt_must_read_memory(self) -> None:
        skill = read_text(SKILL_MD)
        self.assertIn("./.co-improvement/learnt/contexts/", skill)
        self.assertIn("./.co-improvement/learnt/rubrics/index.json", skill)
        self.assertRegex(skill, r"(?i)Read memory files first")

    def test_state_3_is_audit_gate_not_writer(self) -> None:
        skill = read_text(SKILL_MD)
        state3 = skill.split("### State 3")[1].split("### State 4")[0]
        self.assertRegex(state3, r"(?i)fallback review|audit")
        self.assertIn("PERSIST_OK", state3)
        self.assertIn("subagent", state3.lower())
        self.assertIn("$persist-rubrics-context", state3)

    def test_host_requires_subagent_ran_and_log_updated(self) -> None:
        skill = read_text(SKILL_MD)
        self.assertNotIn(
            "Always produce write-ready JSON memory updates for both context and rubric branches.",
            skill,
        )
        self.assertRegex(
            skill,
            r"(?i)Response|learning_log_row|Learning Log was merged|session Learning Log",
        )

    def test_bootstrap_points_at_persist_skill(self) -> None:
        combined = f"{read_text(SKILL_MD)}\n{read_text(LOCAL_SKILL_OUTPUT)}\n{read_text(PERSIST_POINTER)}"
        self.assertIn("persist_rubrics_context_skill_dir", combined)
        self.assertNotIn(
            "<co_improvement_adapt_skill_dir>/scripts/bootstrap_memory_artifacts.sh",
            combined,
        )

    def test_skill_md_does_not_list_local_memory_protocol(self) -> None:
        skill = read_text(SKILL_MD)
        # Local adapt paths only (persist skill may still be pointed at)
        self.assertNotRegex(skill, r"(?m)^- `references/memory-protocol\.md`")
        self.assertNotRegex(skill, r"(?m)^- `references/context-persistence-rubric\.md`")
        self.assertNotRegex(skill, r"(?m)^- `references/rubric-persistence-rubric\.md`")
        self.assertNotRegex(skill, r"(?m)^- `references/rubric-entry-template\.md`")
        self.assertIn("persist-rubrics-context", skill)
        self.assertIn(
            "persist-rubrics-context/references/memory-protocol.md",
            skill,
        )

    def test_pointer_doc_roots_assets_under_persist_skill(self) -> None:
        pointer = read_text(PERSIST_POINTER)
        self.assertIn("call-contract.md", pointer)
        self.assertIn(
            "${CODEX_HOME:-$HOME/.codex}/skills/persist-rubrics-context/",
            pointer,
        )
        self.assertIn("one-way import", pointer.lower().replace("one-way", "one-way"))
        self.assertRegex(pointer, r"(?i)client adapter|one-way import|imports")

    def test_local_skill_memory_interface_is_subagent_write(self) -> None:
        local = read_text(LOCAL_SKILL_OUTPUT)
        self.assertIn("subagent(`$persist-rubrics-context`)", local)
        self.assertRegex(
            local,
            r"(?i)Memory Interface.*read|reads.*subagent",
        )
        self.assertNotRegex(
            local,
            r'(?m)reads, writes, or references project',
        )

    def test_agents_prompt_mentions_persist_subagent(self) -> None:
        agents = read_text(ROOT / "agents" / "openai.yaml")
        self.assertIn("persist-rubrics-context", agents)
        self.assertIn("subagent", agents.lower())


if __name__ == "__main__":
    unittest.main()

