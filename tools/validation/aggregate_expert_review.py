#!/usr/bin/env python3
"""Aggregate expert questionnaire responses into the review matrix.

Reads the item matrix produced by generate_expert_review.py and every response
file exported by the questionnaire (validation/expert-review/responses/*.json),
then updates each item's `status` in place and writes an adjudication report.

Adjudication rules (see validation/expert-review/README.md):
- `pending`  : no expert has answered the item yet;
- `validé`   : every collected answer agrees with the catalog position
               (`expected`), with no « Ça dépend »;
- `contesté` : at least one « Ça dépend », a disagreement between experts, an
               answer contradicting the catalog, or a gap reported on an open
               question (any answer other than « RAS »).
Items marked `covered_by` inherit the status of their covering item.

Usage:
    python tools/validation/aggregate_expert_review.py \
        --matrix validation/expert-review/items_escort-v0.1.yaml
"""

from __future__ import annotations

import argparse
import datetime
import json
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[2]
DEFAULT_RESPONSES = ROOT / "validation" / "expert-review" / "responses"

VALIDATED = "validé"
CONTESTED = "contesté"
PENDING = "pending"


def load_responses(responses_dir: Path, campaign: str) -> list[dict]:
    responses = []
    for path in sorted(responses_dir.glob("*.json")):
        data = json.loads(path.read_text(encoding="utf-8"))
        if data.get("campaign") != campaign:
            print(f"ignoré (autre campagne) : {path.name}", file=sys.stderr)
            continue
        responses.append(data)
    return responses


def collect_answers(item_id: str, responses: list[dict]) -> list[dict]:
    answers = []
    for response in responses:
        answer = response.get("answers", {}).get(item_id)
        if answer is not None:
            answers.append({
                "expert": response.get("expert", "?"),
                "value": answer.get("value"),
                "comment": (answer.get("comment") or "").strip(),
            })
    return answers


def adjudicate(item: dict, answers: list[dict]) -> tuple[str, list[str]]:
    if not answers:
        return PENDING, []
    reasons = []
    question = item.get("question", {})
    expected = question.get("expected")
    is_open = question.get("format") == "open"

    if is_open:
        gaps = [a for a in answers if a["comment"].strip().lower().rstrip(".") != "ras"]
        if gaps:
            return CONTESTED, [f"manque signalé par {a['expert']} : {a['comment']}" for a in gaps]
        return VALIDATED, []

    depends = [a for a in answers if a["value"] == "Ça dépend"]
    for answer in depends:
        reasons.append(f"« Ça dépend » ({answer['expert']}) : {answer['comment']}")

    firm_values = {a["value"] for a in answers if a["value"] != "Ça dépend"}
    if len(firm_values) > 1:
        detail = ", ".join(f"{a['expert']} → {a['value']}" for a in answers)
        reasons.append(f"désaccord entre experts : {detail}")
    if expected and expected != "Ça dépend" and firm_values - {expected}:
        dissent = [a for a in answers if a["value"] not in (expected, "Ça dépend")]
        for answer in dissent:
            note = f" — {answer['comment']}" if answer["comment"] else ""
            reasons.append(f"contredit le catalogue ({answer['expert']} → {answer['value']}{note})")

    return (CONTESTED, reasons) if reasons else (VALIDATED, [])


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--matrix", type=Path, required=True)
    parser.add_argument("--responses", type=Path, default=DEFAULT_RESPONSES)
    args = parser.parse_args()

    matrix = yaml.safe_load(args.matrix.read_text(encoding="utf-8"))
    campaign = matrix.get("campaign", "?")
    if not args.responses.is_dir():
        print(f"Aucun dossier de réponses : {args.responses}", file=sys.stderr)
        return 1
    responses = load_responses(args.responses, campaign)
    if not responses:
        print("Aucune réponse collectée pour cette campagne : rien à agréger.")
        return 0

    items = matrix["items"]
    by_id = {item["id"]: item for item in items}
    contested_details: dict[str, list[str]] = {}

    for item in items:
        if "covered_by" in item:
            continue
        answers = collect_answers(item["id"], responses)
        status, reasons = adjudicate(item, answers)
        item["status"] = status
        # The repository is public. Keep identities in local response/report
        # files only; the tracked matrix carries aggregate evidence.
        item.pop("reviewers", None)
        item["reviewer_count"] = len({a["expert"] for a in answers})
        if reasons:
            contested_details[item["id"]] = reasons
    for item in items:
        if "covered_by" in item:
            covering = by_id[item["covered_by"]]
            item["status"] = covering["status"]
            item.pop("reviewers", None)
            item["reviewer_count"] = covering.get("reviewer_count", 0)

    matrix["last_aggregation"] = {
        "date": datetime.date.today().isoformat(),
        "response_count": len(responses),
        "reviewer_count": len({r.get("expert", "?") for r in responses}),
    }
    args.matrix.write_text(
        yaml.safe_dump(matrix, allow_unicode=True, sort_keys=False, width=100),
        encoding="utf-8")

    counts = {PENDING: 0, VALIDATED: 0, CONTESTED: 0}
    for item in items:
        counts[item["status"]] = counts.get(item["status"], 0) + 1
    total = len(items)

    report_path = args.matrix.parent / f"report_{campaign}.md"
    lines = [
        f"# Rapport d'adjudication — campagne {campaign}",
        "",
        f"> Généré le {datetime.date.today().isoformat()} à partir de "
        f"{len(responses)} réponse(s) : {', '.join(r.get('expert', '?') for r in responses)}.",
        "",
        f"**Couverture : {counts[VALIDATED]} validé(s), {counts[CONTESTED]} contesté(s), "
        f"{counts[PENDING]} en attente, sur {total} items.**",
        "",
    ]
    if contested_details:
        lines.append("## Items contestés (ordre du jour d'adjudication)")
        lines.append("")
        for item_id, reasons in contested_details.items():
            item = by_id[item_id]
            statement = item.get("question", {}).get("statement", "").strip()
            expected = item.get("question", {}).get("expected")
            lines.append(f"### {item_id}")
            lines.append("")
            lines.append(f"> {statement}")
            if expected:
                lines.append(f">\n> *Position du catalogue : {expected}*")
            lines.append("")
            for reason in reasons:
                lines.append(f"- {reason}")
            lines.append("")
    else:
        lines.append("Aucun item contesté : pas d'atelier d'adjudication nécessaire.")
        lines.append("")
    report_path.write_text("\n".join(lines), encoding="utf-8")

    print(f"{counts[VALIDATED]}/{total} validés, {counts[CONTESTED]} contestés, "
          f"{counts[PENDING]} en attente.")
    def display(path: Path) -> Path:
        try:
            return path.relative_to(ROOT)
        except ValueError:
            return path

    print(f"Matrice mise à jour : {display(args.matrix)}")
    print(f"Rapport : {display(report_path)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
