#!/usr/bin/env python3
# Tests SKILL.md / references semantics for event-driven State 3 (persist)
# and State 4 (reflect), plus mandatory fallback closeout gates.

from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
SKILL_MD = ROOT / "SKILL.md"
PERSIST_SKILL = ROOT / "references" / "persist-learnings-skill.md"
REFLECTION = ROOT / "references" / "reflection-paradigm.md"
LOCAL_SKILL_OUTPUT = ROOT / "references" / "local-skill-output.md"
META_METHOD = ROOT / "references" / "meta-method.md"
# Memory protocol lives only under $persist-rubrics-context


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


class EventDrivenPersistReflectSemanticsTest(unittest.TestCase):
    def test_section_loop_is_not_rigid_2_3_4_pipeline(self) -> None:
        skill_text = read_text(SKILL_MD)
        self.assertNotIn(
            "For each draft section, run State 2 → State 3 → State 4 in order.",
            skill_text,
        )
        self.assertIn("event-driven", skill_text.lower())
        self.assertIn("fallback", skill_text.lower())

    def test_persist_is_separate_skill_triggered_on_feedback(self) -> None:
        skill_text = read_text(SKILL_MD)
        persist_text = read_text(PERSIST_SKILL)
        combined = f"{skill_text}\n{persist_text}"

        self.assertTrue(PERSIST_SKILL.is_file())
        self.assertIn("persist-rubrics-context", combined)
        self.assertIn("$persist-rubrics-context", skill_text)
        self.assertRegex(
            skill_text,
            r"(?i)subagent\(`?\$persist-rubrics-context`?\)|spawn a \*\*subagent\*\*.{0,80}persist-rubrics-context",
        )
        self.assertIn("subagent", read_text(PERSIST_SKILL).lower())
        self.assertRegex(
            combined,
            r"(?i)(human (feedback|provides)|when the human provides).{0,120}(rubric|context)",
        )

    def test_standalone_persist_skill_is_installed(self) -> None:
        import os

        codex = Path(os.environ["CODEX_HOME"]) if os.environ.get("CODEX_HOME") else Path.home() / ".codex"
        standalone = codex / "skills" / "persist-rubrics-context" / "SKILL.md"
        self.assertTrue(
            standalone.is_file(),
            f"expected {standalone}",
        )
        text = standalone.read_text(encoding="utf-8")
        self.assertIn("name: persist-rubrics-context", text)

    def test_learning_log_supports_pending_and_decided(self) -> None:
        import os

        codex = Path(os.environ["CODEX_HOME"]) if os.environ.get("CODEX_HOME") else Path.home() / ".codex"
        standalone = (codex / "skills" / "persist-rubrics-context" / "SKILL.md").read_text(
            encoding="utf-8"
        )
        skill_text = read_text(SKILL_MD)
        combined = f"{skill_text}\n{standalone}"
        self.assertRegex(combined, r"(?i)status\s*=\s*`?pending")
        self.assertRegex(combined, r"(?i)status\s*=\s*`?decided|`?decided`?")
        self.assertIn("pending", standalone.lower())
        self.assertRegex(
            skill_text,
            r"(?i)pending.{0,80}(resolve|PERSIST_OK|before `PERSIST_OK`)",
        )
        self.assertRegex(
            standalone + "\n" + (codex / "skills" / "persist-rubrics-context" / "references" / "call-contract.md").read_text(encoding="utf-8"),
            r"(?i)learning_log_row|Learning Log",
        )

    def test_no_memory_write_without_human_decision(self) -> None:
        import os

        codex = Path(os.environ["CODEX_HOME"]) if os.environ.get("CODEX_HOME") else Path.home() / ".codex"
        skill_root = codex / "skills" / "persist-rubrics-context"
        persist_text = (skill_root / "SKILL.md").read_text(encoding="utf-8")
        memory_text = (skill_root / "references" / "memory-protocol.md").read_text(encoding="utf-8")
        self.assertRegex(
            persist_text,
            r"(?i)Never write memory without an explicit human decision",
        )
        self.assertRegex(
            memory_text,
            r"(?i)Precondition:.*status=decided|Learning Log `status=decided`|decision_mode",
        )
        self.assertNotRegex(
            memory_text,
            r"(?i)If `append` vs `merge` is ambiguous, ask human before writing",
        )

    def test_state_3_fallback_reviews_already_persisted_learnings(self) -> None:
        skill_text = read_text(SKILL_MD)
        self.assertIn("State 3", skill_text)
        self.assertIn("fallback", skill_text.lower())
        self.assertIn("PERSIST_OK", skill_text)
        self.assertRegex(
            skill_text,
            r"(?i)review.{0,60}(persisted|learnt|learning|memory)",
        )

    def test_state_3_always_scans_for_missed_candidates(self) -> None:
        skill_text = read_text(SKILL_MD)
        self.assertIn("missed-candidate scan", skill_text)
        state3 = skill_text.split("### State 3")[1].split("### State 4")[0]
        self.assertIn("missed-candidate scan", state3)
        self.assertIn("PERSIST_OK", state3)
        self.assertIn("Human Score Rationale Log", state3)
        self.assertIn("state3-missed-scan", state3)

    def test_state_2_interrupts_are_continuous_not_only_mid_list(self) -> None:
        skill_text = read_text(SKILL_MD)
        self.assertRegex(
            skill_text,
            r"(?i)Continuous interrupts while in State 2",
        )
        # Learn/reflect should not appear only as ordered steps 7-8 in the main list
        self.assertNotRegex(
            skill_text,
            r"(?m)^\d+\.\s+\*\*Learn interrupt:\*\*",
        )

    def test_reflection_triggerable_anytime_and_fallback_closeout(self) -> None:
        skill_text = read_text(SKILL_MD)
        reflection_text = read_text(REFLECTION)
        combined = f"{skill_text}\n{reflection_text}"

        self.assertRegex(combined, r"(?i)any\s*time|anytime|at any time")
        self.assertIn("REFLECT_OK", skill_text)
        self.assertRegex(
            combined,
            r"(?i)(fallback|closeout).{0,80}reflect",
        )
        self.assertRegex(
            combined,
            r"(?i)(already|captured|happened).{0,40}reflect",
        )

    def test_reflection_trigger_is_not_over_broad(self) -> None:
        skill_text = read_text(SKILL_MD)
        reflection_text = read_text(REFLECTION)
        combined = f"{skill_text}\n{reflection_text}"
        self.assertNotIn(
            "unsolicited human reflection content",
            skill_text,
        )
        self.assertRegex(
            combined,
            r"(?i)(explicit|asks to reflect|labeled as reflection)",
        )

    def test_anytime_reflection_defaults_low_budget_when_unknown(self) -> None:
        skill_text = read_text(SKILL_MD)
        reflection_text = read_text(REFLECTION)
        combined = f"{skill_text}\n{reflection_text}"
        self.assertRegex(
            combined,
            r"(?i)(default|defaults).{0,40}(to )?`?low`?",
        )

    def test_nested_interrupts_resume_closeout(self) -> None:
        skill_text = read_text(SKILL_MD)
        self.assertRegex(
            skill_text,
            r"(?i)nested interrupt",
        )
        self.assertRegex(
            skill_text,
            r"(?i)only State 4 fallback.{0,40}REFLECT_OK",
        )

    def test_review_ok_does_not_force_full_persist_then_reflect_pipeline(self) -> None:
        skill_text = read_text(SKILL_MD)
        self.assertNotIn(
            "Transition to State 3 only after `REVIEW_OK`.",
            skill_text,
        )
        self.assertNotIn(
            "Transition to State 4 only after `PERSIST_OK`.",
            skill_text,
        )
        self.assertIn("REVIEW_OK", skill_text)
        self.assertRegex(
            skill_text,
            r"(?i)REVIEW_OK.{0,200}(fallback|closeout|State 3)",
        )

    def test_resume_prior_state_and_no_section_advance_on_interrupt(self) -> None:
        import os

        codex = Path(os.environ["CODEX_HOME"]) if os.environ.get("CODEX_HOME") else Path.home() / ".codex"
        standalone = (codex / "skills" / "persist-rubrics-context" / "SKILL.md").read_text(
            encoding="utf-8"
        )
        skill_text = read_text(SKILL_MD)
        combined = f"{skill_text}\n{standalone}"
        self.assertRegex(
            combined,
            r"(?i)resume.{0,60}(prior|interrupted|host)",
        )
        self.assertRegex(
            combined,
            r"(?i)do \*\*not\*\* advance|do not count as section advance|without advancing",
        )

    def test_embedded_lifecycle_allows_event_and_fallback_persistence(self) -> None:
        local = read_text(LOCAL_SKILL_OUTPUT)
        self.assertRegex(
            local,
            r"(?i)(event-driven|interrupt|anytime|any time).{0,80}(persist|reflect|learning)",
        )
        self.assertRegex(
            local,
            r"(?i)(persist-learnings|Learning Log|PERSIST_OK)",
        )

    def test_meta_method_embedded_lifecycle_matches_event_model(self) -> None:
        meta = read_text(META_METHOD)
        self.assertRegex(
            meta,
            r"(?i)event-driven",
        )
        self.assertRegex(
            meta,
            r"(?i)(anytime|any time).{0,40}reflect",
        )
        self.assertRegex(
            meta,
            r"(?i)fallback",
        )

    def test_memory_protocol_points_at_event_driven_write_path(self) -> None:
        import os

        codex = Path(os.environ["CODEX_HOME"]) if os.environ.get("CODEX_HOME") else Path.home() / ".codex"
        memory = (
            codex / "skills" / "persist-rubrics-context" / "references" / "memory-protocol.md"
        ).read_text(encoding="utf-8")
        self.assertIn("$persist-rubrics-context", memory)
        self.assertIn("call-contract.md", memory)
        self.assertRegex(
            memory,
            r"(?i)learning_log_row|Learning Log",
        )


if __name__ == "__main__":
    unittest.main()
