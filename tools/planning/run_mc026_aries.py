"""Parse and solve the experimental MC-026 HDDL pilot with Aries."""

from __future__ import annotations

import argparse
import json
import sys
from importlib.metadata import version
from pathlib import Path

from unified_planning.engines.results import PlanGenerationResultStatus
from unified_planning.io import PDDLReader
from unified_planning.shortcuts import OneshotPlanner


ROOT = Path(__file__).resolve().parents[2]
DEFAULT_FRAGMENT = ROOT / "references/hddl/experimental/mc-026-close-guard"
OUTPUT_ROOT = ROOT / "outputs"
DEFAULT_OUTPUT = Path("mc-026/aries-plan.json")
EXPECTED_PLAN = (
    "start-follow-designated-unit(escort-1, protected-hvu-1)",
    "start-guard-object(escort-1, protected-hvu-1)",
    "navigate-route(protected-hvu-1, escort-route-1, transit-destination, transit-origin)",
    "evaluate-escort-destination(protected-hvu-1, escort-route-1, transit-destination)",
    "stop-guard-object(escort-1, protected-hvu-1)",
    "stop-follow-designated-unit(escort-1, protected-hvu-1)",
)


def primitive_actions(result: object) -> tuple[str, ...]:
    """Return the ordered primitive plan exposed by Unified Planning."""

    plan = getattr(result, "plan", None)
    action_plan = getattr(plan, "action_plan", None)
    if action_plan is None:
        return ()
    return tuple(str(action) for action in action_plan.actions)


def result_document(result: object, domain: Path, problem: Path) -> dict[str, object]:
    """Build the stable, machine-readable result exported by this pilot."""

    plan = result.plan
    methods = [
        {
            "name": method_instance.method.name,
            "parameters": [str(parameter) for parameter in method_instance.parameters],
        }
        for _, method_instance in plan.methods()
    ]
    actions = [
        {
            "step": index,
            "name": action.action.name,
            "parameters": [str(parameter) for parameter in action.actual_parameters],
        }
        for index, action in enumerate(plan.action_plan.actions, start=1)
    ]

    def repository_path(path: Path) -> str:
        resolved = path.resolve()
        try:
            return resolved.relative_to(ROOT).as_posix()
        except ValueError:
            return str(resolved)

    return {
        "schema_version": "1.0",
        "scenario": {
            "mission_id": "MC-026",
            "method_catalog_id": "TM-023-S01-M01",
        },
        "planner": {
            "name": "Aries",
            "version": version("up-aries"),
            "interface": "Unified Planning",
            "interface_version": version("unified-planning"),
        },
        "status": result.status.name,
        "inputs": {
            "domain": repository_path(domain),
            "problem": repository_path(problem),
        },
        "selected_methods": methods,
        "primitive_plan": actions,
    }


def safe_output_path(output: Path) -> Path:
    """Resolve an output path while confining it to the repository output root."""

    if output.is_absolute():
        raise ValueError("The output path must be relative to the outputs directory.")
    output_root = OUTPUT_ROOT.resolve()
    resolved = (output_root / output).resolve()
    if resolved == output_root or not resolved.is_relative_to(output_root):
        raise ValueError("The output path must remain inside the outputs directory.")
    return resolved


def write_result(document: dict[str, object], output: Path) -> Path:
    """Write a deterministic UTF-8 JSON result."""

    resolved_output = safe_output_path(output)
    resolved_output.parent.mkdir(parents=True, exist_ok=True)
    resolved_output.write_text(
        json.dumps(document, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    return resolved_output


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Validate the MC-026 HDDL pilot with Unified Planning and Aries."
    )
    parser.add_argument("--domain", type=Path, default=DEFAULT_FRAGMENT / "domain.hddl")
    parser.add_argument("--problem", type=Path, default=DEFAULT_FRAGMENT / "problem.hddl")
    parser.add_argument(
        "--output",
        type=Path,
        default=DEFAULT_OUTPUT,
        help="JSON path relative to outputs/ (default: mc-026/aries-plan.json).",
    )
    args = parser.parse_args()

    problem = PDDLReader().parse_problem(str(args.domain), str(args.problem))
    with OneshotPlanner(name="aries") as planner:
        result = planner.solve(problem)

    solved_statuses = {
        PlanGenerationResultStatus.SOLVED_SATISFICING,
        PlanGenerationResultStatus.SOLVED_OPTIMALLY,
    }
    if result.status not in solved_statuses:
        print(f"Aries did not solve the pilot: {result.status.name}", file=sys.stderr)
        return 1

    actual_plan = primitive_actions(result)
    if actual_plan != EXPECTED_PLAN:
        print("Aries returned an unexpected primitive plan:", file=sys.stderr)
        for index, action in enumerate(actual_plan, start=1):
            print(f"  {index}. {action}", file=sys.stderr)
        return 1

    document = result_document(result, args.domain, args.problem)
    selected_method_names = [method["name"] for method in document["selected_methods"]]
    if selected_method_names != ["close-guard-route-escort"]:
        print(
            f"Aries returned unexpected HTN methods: {selected_method_names}",
            file=sys.stderr,
        )
        return 1

    try:
        output_path = write_result(document, args.output)
    except ValueError as error:
        parser.error(str(error))

    print(f"Planner: Aries | Status: {result.status.name}")
    for index, action in enumerate(actual_plan, start=1):
        print(f"{index}. {action}")
    print("MC-026 primitive plan matches the expected start/stop lifecycle.")
    print(f"JSON result: {output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
