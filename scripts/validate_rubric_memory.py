#!/usr/bin/env python3
import argparse
import json
import re
from pathlib import Path

REQUIRED_INDEX_KEYS = {
    "id",
    "path",
    "status",
    "intent_keywords",
    "context_keywords",
    "applicability_summary",
}
FORBIDDEN_INDEX_KEYS = {"priority", "version", "supersedes"}
REQUIRED_RUBRIC_KEYS = {
    "id",
    "title",
    "applicability",
    "decision_rule",
    "dependencies",
    "lifecycle",
}
REQUIRED_CONTEXT_KEYS = {
    "id",
    "statement",
    "intent_keywords",
    "context_keywords",
    "scope",
    "lifecycle",
}


def load_json(path: Path):
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def is_non_empty_string(value) -> bool:
    return isinstance(value, str) and value.strip() != ""


def is_string_list(value) -> bool:
    return isinstance(value, list) and len(value) > 0 and all(is_non_empty_string(x) for x in value)


def resolve_index_path(project_root: Path, path_value: str):
    if not is_non_empty_string(path_value):
        return None, "path must be non-empty string"

    candidate = Path(path_value)
    if candidate.is_absolute():
        return None, "path must be relative to project root"

    target_path = (project_root / candidate).resolve()
    try:
        target_path.relative_to(project_root)
    except ValueError:
        return None, "path escapes project root"

    return target_path, None


def validate_index(index_path: Path, project_root: Path):
    errors = []
    warnings = []

    try:
        data = load_json(index_path)
    except Exception as exc:
        return [f"{index_path}: invalid JSON ({exc})"], warnings, []

    if not isinstance(data, list):
        return [f"{index_path}: root must be a JSON array"], warnings, []

    if not data:
        warnings.append(f"{index_path}: index is empty")

    active_by_id: dict[str, int] = {}
    rows = []

    for row_no, row in enumerate(data, start=1):
        if not isinstance(row, dict):
            errors.append(f"{index_path}: row {row_no} must be an object")
            continue

        keys = set(row.keys())
        missing = sorted(REQUIRED_INDEX_KEYS - keys)
        if missing:
            errors.append(f"{index_path}: row {row_no} missing keys {missing}")

        forbidden = sorted(FORBIDDEN_INDEX_KEYS.intersection(keys))
        if forbidden:
            errors.append(f"{index_path}: row {row_no} forbidden keys present {forbidden}")

        rid = row.get("id", "")
        status = row.get("status", "")
        path_value = row.get("path", "")

        if not is_non_empty_string(rid):
            errors.append(f"{index_path}: row {row_no} invalid id")
            continue

        if status not in {"active", "deprecated"}:
            errors.append(f"{index_path}: row {row_no} id={rid} invalid status '{status}'")

        if status == "active":
            active_by_id[rid] = active_by_id.get(rid, 0) + 1

        target_path, path_error = resolve_index_path(project_root, path_value)
        if path_error:
            errors.append(f"{index_path}: row {row_no} id={rid} {path_error}")
        else:
            if not target_path.exists():
                errors.append(f"{index_path}: row {row_no} id={rid} path does not exist: {path_value}")
            elif target_path.suffix.lower() != ".json":
                errors.append(f"{index_path}: row {row_no} id={rid} path must end with .json")

        if not is_string_list(row.get("intent_keywords", [])):
            errors.append(f"{index_path}: row {row_no} id={rid} intent_keywords must be non-empty string list")

        if not is_string_list(row.get("context_keywords", [])):
            errors.append(f"{index_path}: row {row_no} id={rid} context_keywords must be non-empty string list")

        if not is_non_empty_string(row.get("applicability_summary", "")):
            errors.append(f"{index_path}: row {row_no} id={rid} applicability_summary must be non-empty string")

        rows.append((row_no, row))

    for rid, count in sorted(active_by_id.items()):
        if count > 1:
            errors.append(f"{index_path}: id={rid} has {count} active rows; ask human to resolve")

    return errors, warnings, rows


def validate_counter_pairs(value, key_name: str):
    if not isinstance(value, list) or len(value) == 0:
        return [f"{key_name} must be a non-empty list"]

    issues = []
    for idx, pair in enumerate(value, start=1):
        if not isinstance(pair, list) or len(pair) != 2:
            issues.append(f"{key_name}[{idx}] must be [counter+, counter-]")
            continue

        plus, minus = pair
        if not is_non_empty_string(plus):
            issues.append(f"{key_name}[{idx}][0] must be non-empty string")
        if not is_non_empty_string(minus):
            issues.append(f"{key_name}[{idx}][1] must be non-empty string")

    return issues


def validate_context_file(path: Path):
    errors = []

    try:
        data = load_json(path)
    except Exception as exc:
        return [f"{path}: invalid JSON ({exc})"]

    if not isinstance(data, dict):
        return [f"{path}: root must be object"]

    missing_keys = sorted(REQUIRED_CONTEXT_KEYS - set(data.keys()))
    if missing_keys:
        errors.append(f"{path}: missing keys {missing_keys}")

    if not is_non_empty_string(data.get("id", "")):
        errors.append(f"{path}: id must be non-empty string")

    if not is_non_empty_string(data.get("statement", "")):
        errors.append(f"{path}: statement must be non-empty string")

    if not is_string_list(data.get("intent_keywords", [])):
        errors.append(f"{path}: intent_keywords must be non-empty string list")

    if not is_string_list(data.get("context_keywords", [])):
        errors.append(f"{path}: context_keywords must be non-empty string list")

    scope = data.get("scope", {})
    if not isinstance(scope, dict):
        errors.append(f"{path}: scope must be object")
    else:
        if not is_string_list(scope.get("include", [])):
            errors.append(f"{path}: scope.include must be non-empty string list")
        if not is_string_list(scope.get("exclude", [])):
            errors.append(f"{path}: scope.exclude must be non-empty string list")

    lifecycle = data.get("lifecycle", {})
    if not isinstance(lifecycle, dict):
        errors.append(f"{path}: lifecycle must be object")

    return errors


def validate_rubric_file(path: Path, expected_id: str):
    errors = []

    try:
        data = load_json(path)
    except Exception as exc:
        return [f"{path}: invalid JSON ({exc})"]

    if not isinstance(data, dict):
        return [f"{path}: root must be object"]

    missing_keys = sorted(REQUIRED_RUBRIC_KEYS - set(data.keys()))
    if missing_keys:
        errors.append(f"{path}: missing keys {missing_keys}")

    rid = data.get("id", "")
    if not is_non_empty_string(rid):
        errors.append(f"{path}: id must be non-empty string")
    elif rid != expected_id:
        errors.append(f"{path}: id mismatch (index id='{expected_id}', file id='{rid}')")

    if not is_non_empty_string(data.get("title", "")):
        errors.append(f"{path}: title must be non-empty string")

    applicability = data.get("applicability", {})
    if not isinstance(applicability, dict):
        errors.append(f"{path}: applicability must be object")
    else:
        if not is_string_list(applicability.get("include", [])):
            errors.append(f"{path}: applicability.include must be non-empty string list")
        if not is_string_list(applicability.get("exclude", [])):
            errors.append(f"{path}: applicability.exclude must be non-empty string list")

    dependencies = data.get("dependencies", {})
    if not isinstance(dependencies, dict):
        errors.append(f"{path}: dependencies must be object")
    else:
        if not is_string_list(dependencies.get("context_refs", [])):
            errors.append(f"{path}: dependencies.context_refs must be non-empty string list")
        if not is_string_list(dependencies.get("intent_refs", [])):
            errors.append(f"{path}: dependencies.intent_refs must be non-empty string list")

    lifecycle = data.get("lifecycle", {})
    if not isinstance(lifecycle, dict):
        errors.append(f"{path}: lifecycle must be object")

    decision_rule = data.get("decision_rule", {})
    if not isinstance(decision_rule, dict):
        errors.append(f"{path}: decision_rule must be object")
        return errors

    score_levels = set()
    pattern = re.compile(r"^score_(\d+)_rule$")
    for key in decision_rule.keys():
        match = pattern.match(key)
        if match:
            score_levels.add(match.group(1))

    if not score_levels:
        errors.append(f"{path}: decision_rule has no score_X_rule keys")
        return errors

    for score in sorted(score_levels):
        rule_key = f"score_{score}_rule"
        support_key = f"score_{score}_support_examples"
        counter_key = f"score_{score}_counter_examples"

        if not is_non_empty_string(decision_rule.get(rule_key, "")):
            errors.append(f"{path}: {rule_key} must be non-empty string")

        support_value = decision_rule.get(support_key)
        if not is_string_list(support_value):
            errors.append(f"{path}: {support_key} must be non-empty string list")

        counter_value = decision_rule.get(counter_key)
        if counter_value is None:
            errors.append(f"{path}: missing {counter_key}")
        else:
            for issue in validate_counter_pairs(counter_value, counter_key):
                errors.append(f"{path}: {issue}")

    return errors


def validate(project_root: Path):
    errors = []
    warnings = []

    contexts_root = project_root / ".co-improvement" / "learnt" / "contexts"
    if contexts_root.exists():
        context_files = sorted(contexts_root.rglob("*.json"))
        for context_path in context_files:
            errors.extend(validate_context_file(context_path))
    else:
        warnings.append(f"Missing contexts directory: {contexts_root}")

    index_path = project_root / ".co-improvement" / "learnt" / "rubrics" / "index.json"
    if not index_path.exists():
        warnings.append(f"Missing rubric index file: {index_path}")
        return errors, warnings

    idx_errors, idx_warnings, rows = validate_index(index_path, project_root)
    errors.extend(idx_errors)
    warnings.extend(idx_warnings)

    for _, row in rows:
        if row.get("status") != "active":
            continue

        path_value = row.get("path", "")
        rid = row.get("id", "")
        if not path_value or not rid:
            continue

        target_path, path_error = resolve_index_path(project_root, path_value)
        if path_error:
            continue

        if target_path.exists():
            errors.extend(validate_rubric_file(target_path, rid))

    return errors, warnings


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Validate JSON-first rubric memory consistency (index.json <-> rubric json files)."
    )
    parser.add_argument(
        "--project-root",
        default=".",
        help="Project root containing .co-improvement/learnt/rubrics/index.json",
    )
    args = parser.parse_args()

    project_root = Path(args.project_root).resolve()
    errors, warnings = validate(project_root)

    print(f"Project root: {project_root}")
    print(f"Errors: {len(errors)}")
    print(f"Warnings: {len(warnings)}")

    if warnings:
        print("\nWarnings:")
        for item in warnings:
            print(f"- {item}")

    if errors:
        print("\nErrors:")
        for item in errors:
            print(f"- {item}")
        return 1

    print("\nValidation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
