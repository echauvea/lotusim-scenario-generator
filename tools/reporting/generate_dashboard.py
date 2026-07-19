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
import html
import json
import os
import re
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
    head = ROOT / ".git" / "HEAD"
    try:
        content = head.read_text(encoding="utf-8").strip()
        if content.startswith("ref: "):
            content = (ROOT / ".git" / content[5:]).read_text(encoding="utf-8").strip()
        return content[:7]
    except OSError:
        return "local"


def load_campaigns(current_versions: dict[str, str]) -> list[dict]:
    """Load campaign matrices as aggregate KPIs only.

    Privacy rule (deliberate): expert names never leave this function — the
    published dashboard and summary only expose reviewer counts. A validation
    recorded against an older catalog version than the current one is counted
    as `stale`, never as still-valid.
    """
    campaigns = []
    for path in sorted(EXPERT_DIR.glob("items_*.yaml")):
        matrix = yaml.safe_load(path.read_text(encoding="utf-8"))
        items = matrix.get("items", [])
        if not items:
            fail(f"campaign matrix without items: {path.name}")
        statuses = [item.get("status", "pending") for item in items]
        reviewer_count = len({name for item in items for name in item.get("reviewers", [])})
        catalog = str(matrix.get("catalog", "?"))
        version = str(matrix.get("catalog_version", "?"))
        prefix = re.sub(r"_v[\d.]+(?:-\w+)?\.\w+$", "", catalog)
        current = current_versions.get(prefix)
        is_stale = current is not None and f"v{version}" != current
        validated = statuses.count("validé")
        campaigns.append({
            "name": matrix.get("campaign", path.stem),
            "target": f"{catalog} ({version})",
            "instrumented": len(items),
            "asked": sum(1 for item in items if "covered_by" not in item),
            "exposed": sum(1 for item in items if item.get("reviewers")),
            "validated": 0 if is_stale else validated,
            "stale": validated if is_stale else 0,
            "contested": statuses.count("contesté"),
            "pending": statuses.count("pending"),
            "reviewer_count": reviewer_count,
            "aggregated": str((matrix.get("last_aggregation") or {}).get("date", "—")),
        })
    return campaigns


def campaign_rows(campaigns: list[dict]) -> str:
    rows = []
    for c in campaigns:
        avancement = pct(c["validated"], c["instrumented"])
        rows.append(
            "          <tr>"
            f"<td><code>{html.escape(c['name'])}</code></td>"
            f"<td>{html.escape(c['target'])}</td>"
            f"<td>{c['instrumented']} ({c['asked']} questions)</td>"
            f"<td>{c['exposed']}</td>"
            f"<td>{c['validated']}</td>"
            f"<td>{c['contested']}</td>"
            f"<td>{c['stale']}</td>"
            f"<td>{c['reviewer_count']}</td>"
            f"<td>{avancement} %</td>"
            "</tr>"
        )
    return "\n".join(rows)


def campaign_cards(campaigns: list[dict]) -> str:
    cards = []
    for c in campaigns:
        avancement = pct(c["validated"], c["instrumented"])
        if c["stale"]:
            etat = f'<span class="etat bloque">{c["stale"]} validation(s) obsolète(s) — le catalogue a évolué depuis la campagne</span>'
        elif not c["reviewer_count"]:
            etat = '<span class="etat attente">en attente d\'experts</span>'
        elif c["contested"]:
            etat = f'<span class="etat partiel">{c["contested"]} contesté(s) à adjuger</span>'
        else:
            etat = '<span class="etat pret">aucun item contesté</span>'
        cards.append(f"""      <div class="voie metier">
        <h3>Campagne <code>{html.escape(c['name'])}</code></h3>
        <div class="mode">cible : {html.escape(c['target'])} · {c['reviewer_count']} relecteur(s) · dernière agrégation : {html.escape(c['aggregated'])}</div>
        <div class="jauge" style="margin-top:8px">
          <div class="jauge-barre"><i class="cuivre" style="width:{avancement}%"></i></div>
          <span class="jauge-val">{c['validated']}/{c['instrumented']} · {avancement} %</span>
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
        method_chips.append(f'<span>{html.escape(short_id)} '
                            f'<span class="etat {css}">{html.escape(readiness)}</span></span>')

    fragments = len(list((ROOT / "references" / "hddl" / "experimental").glob("*/domain.hddl")))

    onto_text = next((ROOT / "references" / "ontology").glob("*.ttl")).read_text(encoding="utf-8")
    onto_version = re.search(r'owl:versionInfo "([^"]+)"', onto_text)
    if not onto_version:
        fail("ontology version not found")

    mc_version = version_from_name("LOTUSim_Mission_Catalog_v*.md", ROOT / "references" / "mission-catalog")
    tc_version = version_from_name("LOTUSim_Task_Catalog_v*.md", ROOT / "references" / "task-catalog")
    tm_version = version_from_name("LOTUSim_Method_Catalog_v*.md", ROOT / "references" / "method-catalog")
    hddl_profile = version_from_name("LOTUSim_HDDL_Profile_v*.md", ROOT / "specification" / "hddl")
    sm_version = f"v{data.state_model['model']['version']}"

    campaigns = load_campaigns({
        "LOTUSim_Mission_Catalog": mc_version,
        "LOTUSim_Task_Catalog": tc_version,
        "LOTUSim_Method_Catalog": tm_version,
    })
    kpi = {key: sum(c[key] for c in campaigns)
           for key in ("instrumented", "exposed", "validated", "contested", "stale")}
    exp_total = kpi["instrumented"]
    exp_valides = kpi["validated"]

    commit = current_commit()
    sm_total = counts["states"] + counts["deferred_candidates"]
    tokens = {
        "__DATE__": datetime.datetime.now(datetime.timezone.utc).strftime("%d/%m/%Y %H:%M UTC"),
        "__COMMIT__": commit,
        "__VALIDATION_SUMMARY__": "passée",
        "__VALIDATION_ETAT__": "100 % passant",
        "__ONTO_VERSION__": html.escape(onto_version.group(1)),
        "__ONTO_CLASSES__": str(len(data.ontology)),
        "__ONTO_CAPACITES__": str(capabilities),
        "__MC_VERSION__": mc_version,
        "__MC_TOTAL__": str(counts["missions"]),
        "__MC_ACTIVES__": str(actives),
        "__MC_CANDIDATES__": str(candidates),
        "__MC_PCT__": str(pct(actives, counts["missions"])),
        "__TC_VERSION__": tc_version,
        "__TC_TACHES__": str(counts["tasks"]),
        "__TC_SIGNATURES__": str(counts["signatures"]),
        "__TC_FAMILLES__": str(counts["families"]),
        "__TC_ENRICHIES__": str(counts["enriched_signatures"]),
        "__TC_PCT__": str(pct(counts["enriched_signatures"], counts["signatures"])),
        "__SM_VERSION__": sm_version,
        "__SM_ETATS__": str(counts["states"]),
        "__SM_TYPES__": str(counts["state_types"]),
        "__SM_DIFFERES__": str(counts["deferred_candidates"]),
        "__SM_TOTAL__": str(sm_total),
        "__SM_PCT__": str(pct(counts["states"], sm_total)),
        "__TM_VERSION__": tm_version,
        "__TM_CHIPS__": "".join(method_chips),
        "__TM_COUVERTES__": str(len(covered)),
        "__TM_ABSTRAITES__": str(len(abstract_ids)),
        "__TM_PCT__": str(pct(len(covered), len(abstract_ids))),
        "__HDDL_PROFIL__": hddl_profile,
        "__HDDL_FRAGMENTS__": str(fragments),
        "__HDDL_PCT__": str(pct(fragments, counts["missions"])),
        "__EXP_TOTAL__": str(exp_total),
        "__EXP_VALIDES__": str(exp_valides),
        "__EXP_PCT__": str(pct(exp_valides, exp_total)),
        "__KPI_INSTRUMENTES__": str(kpi["instrumented"]),
        "__KPI_EXPOSES__": str(kpi["exposed"]),
        "__KPI_VALIDES__": str(kpi["validated"]),
        "__KPI_CONTESTES__": str(kpi["contested"]),
        "__KPI_OBSOLETES__": str(kpi["stale"]),
        "__CAMPAGNES_LIGNES__": campaign_rows(campaigns),
        "__CAMPAGNES_CARTES__": campaign_cards(campaigns),
    }

    summary = {
        "commit": commit,
        "generated_at": datetime.datetime.now(datetime.timezone.utc)
                        .isoformat(timespec="seconds"),
        "referentials": {
            "ontology": {"version": onto_version.group(1), "classes": len(data.ontology),
                         "capabilities": capabilities, "expert_review": None},
            "mission_catalog": {"version": mc_version, "elements": counts["missions"],
                                "candidates": candidates, "expert_review": None},
            "task_catalog": {"version": tc_version, "tasks": counts["tasks"],
                             "signatures": counts["signatures"],
                             "enriched": counts["enriched_signatures"], "expert_review": None},
            "state_model": {"version": sm_version, "states": counts["states"],
                            "deferred": counts["deferred_candidates"], "expert_review": None},
            "method_catalog": {"version": tm_version, "methods": counts["methods"],
                               "abstract_total": len(abstract_ids),
                               "abstract_covered": len(covered), "expert_review": kpi},
            "hddl": {"profile": hddl_profile, "fragments": fragments,
                     "planner_verified": None},
        },
        "campaigns": campaigns,
    }

    page = TEMPLATE.read_text(encoding="utf-8")
    for token, value in tokens.items():
        page = page.replace(token, value)
    leftover = sorted(set(re.findall(r"__[A-Z_]+__", page)))
    if leftover:
        fail(f"unresolved template tokens: {leftover}")

    workspace = Path(os.getenv("GITHUB_WORKSPACE", ROOT)).resolve()
    output = args.output.resolve()
    if not str(output).startswith(str(workspace) + os.sep):
        fail(f"output path must stay inside {workspace}")
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(page, encoding="utf-8")
    # Machine-readable single source of the published indicators (aggregates
    # only — never expert names, free-text answers or adjudication comments).
    summary_path = output.parent / "summary.json"
    summary_path.write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n",
                            encoding="utf-8")
    print(f"Dashboard generated: {output} "
          f"(commit {commit}, {exp_valides}/{exp_total} expert items validated)")
    print(f"Summary JSON: {summary_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
