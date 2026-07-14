#!/usr/bin/env python3
# Tests SKILL.md/local-skill-output.md semantics for generating reusable local skills.

from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
SKILL_MD = ROOT / "SKILL.md"
LOCAL_SKILL_OUTPUT = ROOT / "references" / "local-skill-output.md"


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


class SkillMaterializationSemanticsTest(unittest.TestCase):
    def test_local_skill_mode_requires_materialization_gate(self) -> None:
        skill_text = read_text(SKILL_MD)

        self.assertIn("State 1.5", skill_text)
        self.assertIn("Materialize Local Skill Gate", skill_text)
        self.assertIn("create or update the target local skill folder", skill_text)
        self.assertIn("write the generated `SKILL.md`", skill_text)
        self.assertIn("Transition to State 2 only after", skill_text)

    def test_helper_scripts_are_resolved_from_installed_skill_directories(self) -> None:
        skill_text = read_text(SKILL_MD)
        local_skill_output = read_text(LOCAL_SKILL_OUTPUT)
        combined = f"{skill_text}\n{local_skill_output}"

        self.assertIn("<persist_rubrics_context_skill_dir>/scripts/bootstrap_memory_artifacts.sh", combined)
        self.assertIn("<skill_creator_skill_dir>/scripts/init_skill.py", combined)
        self.assertIn("<skill_creator_skill_dir>/scripts/quick_validate.py", combined)
        self.assertIn("do not assume the target repository has its own `scripts/` folder", combined)


if __name__ == "__main__":
    unittest.main()
