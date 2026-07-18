"""Parse and solve the experimental MC-026 HDDL pilot with Aries."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from unified_planning.engines.results import PlanGenerationResultStatus
from unified_planning.io import PDDLReader
from unified_planning.shortcuts import OneshotPlanner


ROOT = Path(__file__).resolve().parents[2]
DEFAULT_FRAGMENT = ROOT / "references/hddl/experimental/mc-026-close-guard"
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


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Validate the MC-026 HDDL pilot with Unified Planning and Aries."
    )
    parser.add_argument("--domain", type=Path, default=DEFAULT_FRAGMENT / "domain.hddl")
    parser.add_argument("--problem", type=Path, default=DEFAULT_FRAGMENT / "problem.hddl")
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

    print(f"Planner: Aries | Status: {result.status.name}")
    for index, action in enumerate(actual_plan, start=1):
        print(f"{index}. {action}")
    print("MC-026 primitive plan matches the expected start/stop lifecycle.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
