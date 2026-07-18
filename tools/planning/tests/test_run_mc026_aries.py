import json
import unittest
from pathlib import Path
from types import SimpleNamespace
from uuid import uuid4

from tools.planning.run_mc026_aries import (
    OUTPUT_ROOT,
    result_document,
    safe_output_path,
    write_result,
)


class PlannerResultTest(unittest.TestCase):
    def test_result_contains_method_and_structured_primitive_plan(self) -> None:
        method = SimpleNamespace(
            method=SimpleNamespace(name="close-guard-route-escort"),
            parameters=("escort-1", "protected-hvu-1"),
        )
        action = SimpleNamespace(
            action=SimpleNamespace(name="start-follow-designated-unit"),
            actual_parameters=("escort-1", "protected-hvu-1"),
        )
        plan = SimpleNamespace(
            methods=lambda: [("task-id", method)],
            action_plan=SimpleNamespace(actions=(action,)),
        )
        result = SimpleNamespace(
            plan=plan,
            status=SimpleNamespace(name="SOLVED_SATISFICING"),
        )

        document = result_document(result, Path("domain.hddl"), Path("problem.hddl"))

        self.assertEqual(document["scenario"]["mission_id"], "MC-026")
        self.assertEqual(document["selected_methods"][0]["name"], "close-guard-route-escort")
        self.assertEqual(document["primitive_plan"][0]["step"], 1)
        self.assertEqual(
            document["primitive_plan"][0]["name"],
            "start-follow-designated-unit",
        )

    def test_write_result_creates_valid_json(self) -> None:
        relative_output = Path("tests") / f"{uuid4()}.json"
        output = write_result({"status": "SOLVED_SATISFICING"}, relative_output)
        try:
            self.assertEqual(
                json.loads(output.read_text(encoding="utf-8")),
                {"status": "SOLVED_SATISFICING"},
            )
        finally:
            output.unlink(missing_ok=True)

    def test_output_path_cannot_escape_output_directory(self) -> None:
        with self.assertRaises(ValueError):
            safe_output_path(Path("../outside.json"))
        with self.assertRaises(ValueError):
            safe_output_path(OUTPUT_ROOT.parent / "outside.json")


if __name__ == "__main__":
    unittest.main()
