#!/usr/bin/env python3
"""Generate the static LSG referential dashboard published by the CI on GitHub Pages.

Design constraints (deliberate, do not relax without an explicit decision):
- every metric is computed by the same parsers as `validate_referentials.py`
  (imported, not reimplemented), so the dashboard can never drift from what
  the CI validates;
- generation fails — and therefore fails the CI — whenever the referentials
  do not validate, a metric cannot be computed, or a template token is left
  unresolved: the dashboard never silently shows stale or partial figures;
- no history, no scripting beyond tab switching: a faithful snapshot of the
  current baseline, regenerated on every merge.

Usage:
    python tools/reporting/generate_dashboard.py [--output build/dashboard/index.html]
"""

from __future__ import annotations

import argparse
import datetime
import os
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tools" / "validation"))

import yaml  # noqa: E402  (after sys.path setup, same dependency set as the validator)
from validate_referentials import (  # noqa: E402
    ValidationReport, is_ontology_subtype, load_data, validate_repository,
)

TEMPLATE = Path(__file__).resolve().parent / "templates" / "dashboard.html"
EXPERT_DIR = ROOT / "validation" / "expert-review"

READINESS_CLASS = {"ready": "pret", "partial": "partiel", "blocked": "bloque"}


def fail(message: str) -> None:
    print(f"ERROR: {message}", file=sys.stderr)
    sys.exit(1)


def version_from_name(pattern: str, directory: Path) -> str:
    matches = sorted(directory.glob(pattern))
    if len(matches) != 1:
        fail(f"exactly one file matching {pattern} expected in {directory}, found {len(matches)}")
    version = re.search(r"_v([\d.]+(?:-[\w]+)?)\.\w+$", matches[0].name)
    if not version:
        fail(f"no version found in file name {matches[0].name}")
    return f"v{version.group(1)}"


def pct(numerator: int, denominator: int) -> int:
    if denominator <= 0:
        fail(f"invalid denominator for percentage: {numerator}/{denominator}")
    return round(100 * numerator / denominator)


def current_commit() -> str:
    sha = os.getenv("GITHUB_SHA")
    if sha:
        return sha[:7]
    try:
        return subprocess.run(["git", "rev-parse", "--short", "HEAD"], cwd=ROOT,
                              capture_output=True, text=True, check=True).stdout.strip()
    except (OSError, subprocess.CalledProcessError):
        return "local"


def load_campaigns() -> list[dict]:
    campaigns = []
    for path in sorted(EXPERT_DIR.glob("items_*.yaml")):
        matrix = yaml.safe_load(path.read_text(encoding="utf-8"))
        items = matrix.get("items", [])
        if not items:
            fail(f"campaign matrix without items: {path.name}")
        statuses = [item.get("status", "pending") for item in items]
        reviewers = sorted({name for item in items for name in item.get("reviewers", [])})
        campaigns.append({
            "name": matrix.get("campaign", path.stem),
            "target": f"{matrix.get('catalog', '?')} ({matrix.get('catalog_version', '?')})",
            "total": len(items),
            "asked": sum(1 for item in items if "covered_by" not in item),
            "valides": statuses.count("validé"),
            "contestes": statuses.count("contesté"),
            "pending": statuses.count("pending"),
            "reviewers": reviewers,
            "aggregated": (matrix.get("last_aggregation") or {}).get("date", "—"),
        })
    return campaigns


def campaign_rows(campaigns: list[dict]) -> str:
    rows = []
    for c in campaigns:
        avancement = pct(c["valides"], c["total"])
        reviewers = ", ".join(c["reviewers"]) if c["reviewers"] else "—"
        rows.append(
            "          <tr>"
            f"<td><code>{c['name']}</code></td>"
            f"<td>{c['target']}</td>"
            f"<td>{c['total']} ({c['asked']} questions)</td>"
            f"<td>{c['valides']}</td>"
            f"<td>{c['contestes']}</td>"
            f"<td>{c['pending']}</td>"
            f"<td>{reviewers}</td>"
            f"<td>{avancement} %</td>"
            "</tr>"
        )
    return "\n".join(rows)


def campaign_cards(campaigns: list[dict]) -> str:
    cards = []
    for c in campaigns:
        avancement = pct(c["valides"], c["total"])
        etat = ('<span class="etat attente">en attente d\'experts</span>' if not c["reviewers"]
                else f'<span class="etat partiel">{c["contestes"]} contesté(s) à adjuger</span>'
                if c["contestes"] else '<span class="etat pret">aucun item contesté</span>')
        cards.append(f"""      <div class="voie metier">
        <h3>Campagne <code>{c['name']}</code></h3>
        <div class="mode">cible : {c['target']} · dernière agrégation : {c['aggregated']}</div>
        <div class="jauge" style="margin-top:8px">
          <div class="jauge-barre"><i class="cuivre" style="width:{avancement}%"></i></div>
          <span class="jauge-val">{c['valides']}/{c['total']} · {avancement} %</span>
        </div>
        <p class="verdict">{etat}</p>
      </div>""")
    return "\n".join(cards)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=ROOT / "build" / "dashboard" / "index.html")
    args = parser.parse_args()

    report = validate_repository(ROOT)
    if not report.ok:
        for code, location, message in report.errors:
            print(f"ERROR [{code}] {location}: {message}", file=sys.stderr)
        fail("referentials do not validate; dashboard not generated")
    counts = report.counts

    data = load_data(ROOT, ValidationReport())
    if data is None:
        fail("referential data could not be loaded")

    capabilities = sum(
        1 for cls in data.ontology
        if cls != "PhysicalCapability"
        and is_ontology_subtype(cls, "PhysicalCapability", data.ontology_parents)
    )

    candidates = sum(1 for m in data.mission_records if str(m.get("status")) == "candidate")
    actives = counts["missions"] - candidates

    abstract_ids = sorted(
        s["signature_id"] for s in data.signatures
        if (s.get("semantics") or {}).get("semantic_kind") == "abstract"
    )
    covered = sorted({str(m.get("decomposes")) for m in data.method_records})
    uncovered_covered = [c for c in covered if c not in abstract_ids]
    if uncovered_covered:
        fail(f"methods decompose unknown abstract signatures: {uncovered_covered}")

    method_chips = [f"<span><b>{counts['methods']}</b> méthodes</span>"]
    for record in data.method_records:
        readiness = str((record.get("projection") or {}).get("readiness", "?"))
        css = READINESS_CLASS.get(readiness, "attente")
        short_id = str(record.get("id", "?")).rsplit("-", 1)[-1]
        method_chips.append(f'<span>{short_id} <span class="etat {css}">{readiness}</span></span>')

    fragments = len(list((ROOT / "references" / "hddl" / "experimental").glob("*/domain.hddl")))

    onto_text = next((ROOT / "references" / "ontology").glob("*.ttl")).read_text(encoding="utf-8")
    onto_version = re.search(r'owl:versionInfo "([^"]+)"', onto_text)
    if not onto_version:
        fail("ontology version not found")

    campaigns = load_campaigns()
    exp_total = sum(c["total"] for c in campaigns)
    exp_valides = sum(c["valides"] for c in campaigns)

    sm_total = counts["states"] + counts["deferred_candidates"]
    tokens = {
        "__DATE__": datetime.datetime.now(datetime.timezone.utc).strftime("%d/%m/%Y %H:%M UTC"),
        "__COMMIT__": current_commit(),
        "__VALIDATION_SUMMARY__": "passée",
        "__VALIDATION_ETAT__": "100 % passant",
        "__ONTO_VERSION__": onto_version.group(1),
        "__ONTO_CLASSES__": str(len(data.ontology)),
        "__ONTO_CAPACITES__": str(capabilities),
        "__MC_VERSION__": version_from_name("LOTUSim_Mission_Catalog_v*.md", ROOT / "references" / "mission-catalog"),
        "__MC_TOTAL__": str(counts["missions"]),
        "__MC_ACTIVES__": str(actives),
        "__MC_CANDIDATES__": str(candidates),
        "__MC_PCT__": str(pct(actives, counts["missions"])),
        "__TC_VERSION__": version_from_name("LOTUSim_Task_Catalog_v*.md", ROOT / "references" / "task-catalog"),
        "__TC_TACHES__": str(counts["tasks"]),
        "__TC_SIGNATURES__": str(counts["signatures"]),
        "__TC_FAMILLES__": str(counts["families"]),
        "__TC_ENRICHIES__": str(counts["enriched_signatures"]),
        "__TC_PCT__": str(pct(counts["enriched_signatures"], counts["signatures"])),
        "__SM_VERSION__": f"v{data.state_model['model']['version']}",
        "__SM_ETATS__": str(counts["states"]),
        "__SM_TYPES__": str(counts["state_types"]),
        "__SM_DIFFERES__": str(counts["deferred_candidates"]),
        "__SM_TOTAL__": str(sm_total),
        "__SM_PCT__": str(pct(counts["states"], sm_total)),
        "__TM_VERSION__": version_from_name("LOTUSim_Method_Catalog_v*.md", ROOT / "references" / "method-catalog"),
        "__TM_CHIPS__": "".join(method_chips),
        "__TM_COUVERTES__": str(len(covered)),
        "__TM_ABSTRAITES__": str(len(abstract_ids)),
        "__TM_PCT__": str(pct(len(covered), len(abstract_ids))),
        "__HDDL_PROFIL__": version_from_name("LOTUSim_HDDL_Profile_v*.md", ROOT / "specification" / "hddl"),
        "__HDDL_FRAGMENTS__": str(fragments),
        "__HDDL_PCT__": str(pct(fragments, counts["missions"])),
        "__EXP_TOTAL__": str(exp_total),
        "__EXP_VALIDES__": str(exp_valides),
        "__EXP_PCT__": str(pct(exp_valides, exp_total)),
        "__CAMPAGNES_LIGNES__": campaign_rows(campaigns),
        "__CAMPAGNES_CARTES__": campaign_cards(campaigns),
    }

    html = TEMPLATE.read_text(encoding="utf-8")
    for token, value in tokens.items():
        html = html.replace(token, value)
    leftover = sorted(set(re.findall(r"__[A-Z_]+__", html)))
    if leftover:
        fail(f"unresolved template tokens: {leftover}")

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(html, encoding="utf-8")
    print(f"Dashboard generated: {args.output} "
          f"(commit {tokens['__COMMIT__']}, {exp_valides}/{exp_total} expert items validated)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
