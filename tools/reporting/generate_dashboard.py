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
import hashlib
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


def current_catalog_sources(versions: dict[str, str]) -> dict[str, dict[str, str]]:
    locations = {
        "LOTUSim_Mission_Catalog": (
            ROOT / "references" / "mission-catalog", "LOTUSim_Mission_Catalog_v*.md"),
        "LOTUSim_Task_Catalog": (
            ROOT / "references" / "task-catalog", "LOTUSim_Task_Catalog_v*.md"),
        "LOTUSim_Method_Catalog": (
            ROOT / "references" / "method-catalog", "LOTUSim_Method_Catalog_v*.md"),
    }
    sources = {}
    for prefix, (directory, pattern) in locations.items():
        matches = sorted(directory.glob(pattern))
        if len(matches) != 1:
            fail(f"exactly one current catalog expected for {prefix}, found {len(matches)}")
        sources[prefix] = {
            "version": versions[prefix],
            "sha256": hashlib.sha256(matches[0].read_bytes()).hexdigest(),
        }
    return sources


def pct(numerator: int, denominator: int) -> int:
    if denominator <= 0:
        fail(f"invalid denominator for percentage: {numerator}/{denominator}")
    return round(100 * numerator / denominator)


def current_commit() -> str:
    sha = os.getenv("GITHUB_SHA")
    if sha:
        return sha[:7]
    try:
        marker = ROOT / ".git"
        if marker.is_file():
            declaration = marker.read_text(encoding="utf-8").strip()
            if not declaration.startswith("gitdir: "):
                return "local"
            git_dir = (ROOT / declaration[8:]).resolve()
        else:
            git_dir = marker
        common_dir = git_dir
        common_marker = git_dir / "commondir"
        if common_marker.is_file():
            common_dir = (git_dir / common_marker.read_text(encoding="utf-8").strip()).resolve()
        head = git_dir / "HEAD"
        content = head.read_text(encoding="utf-8").strip()
        if content.startswith("ref: "):
            ref = content[5:]
            ref_path = common_dir / ref
            if not ref_path.is_file():
                return "local"
            content = ref_path.read_text(encoding="utf-8").strip()
        return content[:7]
    except OSError:
        return "local"


def load_campaigns(current_sources: dict[str, dict[str, str]]) -> list[dict]:
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
        aggregation = matrix.get("last_aggregation") or {}
        if any("reviewers" in item for item in items) or "responses" in aggregation:
            fail(f"campaign matrix contains expert identities: {path.name}")
        reviewer_count = int(aggregation.get("reviewer_count", 0))
        catalog = str(matrix.get("catalog", "?"))
        version = str(matrix.get("catalog_version", "?"))
        prefix = re.sub(r"_v[\d.]+(?:-\w+)?\.\w+$", "", catalog)
        current = current_sources.get(prefix)
        catalog_sha256 = matrix.get("catalog_sha256")
        version_changed = current is not None and f"v{version}" != current["version"]
        content_changed = (current is not None and catalog_sha256 is not None
                           and catalog_sha256 != current["sha256"])
        is_stale = version_changed or content_changed
        validated = statuses.count("validé")
        campaigns.append({
            "name": matrix.get("campaign", path.stem),
            "target": f"{catalog} ({version})",
            "catalog_prefix": prefix,
            "instrumented": len(items),
            "asked": sum(1 for item in items if "covered_by" not in item),
            "exposed": sum(1 for item in items if item.get("reviewer_count", 0)),
            "validated": 0 if is_stale else validated,
            "stale": validated if is_stale else 0,
            "contested": statuses.count("contesté"),
            "pending": statuses.count("pending"),
            "reviewer_count": reviewer_count,
            "aggregated": str(aggregation.get("date", "—")),
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


def cell(css: str, big: str, small: str) -> str:
    return f'<td><div class="cellule {css}"><b>{big}</b><span>{small}</span></div></td>'


def matrix_rows(rows: list[dict]) -> str:
    lines = []
    for row in rows:
        cells = [cell("c-inv", row["inventory"], row["inventory_label"])]
        if row["campaigns"]:
            instr = sum(c["instrumented"] for c in row["campaigns"])
            exposed = sum(c["exposed"] for c in row["campaigns"])
            validated = sum(c["validated"] for c in row["campaigns"])
            stale = sum(c["stale"] for c in row["campaigns"])
            valid_label = f"{validated} / {instr} validés"
            if stale:
                valid_label += f" · {stale} obsolètes"
            cells.append(cell("c-instr", str(instr), f"items · {sum(c['asked'] for c in row['campaigns'])} questions"))
            cells.append(cell("c-mesure", f"{pct(exposed, instr)} %", f"{exposed} / {instr} exposés"))
            cells.append(cell("c-mesure", f"{pct(validated, instr)} %", valid_label))
        else:
            cells.append(cell("c-nm", "—", "extracteur absent"))
            cells.append(cell("c-nm", "—", "non mesurable"))
            cells.append(cell("c-nm", "—", "non mesurable"))
        lines.append(f'          <tr><td class="ref-nom">{row["name"]}</td>{"".join(cells)}</tr>')
    return "\n".join(lines)


def callouts(rows: list[dict]) -> str:
    blocks = []
    for row in rows:
        if not row["campaigns"]:
            continue
        instr = sum(c["instrumented"] for c in row["campaigns"])
        asked = sum(c["asked"] for c in row["campaigns"])
        exposed = sum(c["exposed"] for c in row["campaigns"])
        validated = sum(c["validated"] for c in row["campaigns"])
        contested = sum(c["contested"] for c in row["campaigns"])
        stale = sum(c["stale"] for c in row["campaigns"])
        phrase = (f"Le générateur couvre {instr} items du périmètre instrumenté, "
                  f"condensés en {asked} questions. ")
        if stale:
            badge, classe = "instrumenté · obsolescence", "bloque"
            phrase += (f"{stale} validation(s) acquises sur une version antérieure du catalogue "
                       "sont comptées obsolètes et à re-soumettre.")
        elif exposed == 0:
            badge, classe = "instrumenté · en attente", "attente"
            phrase += ("Aucune réponse experte n'a encore été collectée : "
                       "la couverture validée est donc réellement de 0 %.")
        elif contested:
            badge, classe = "instrumenté · à adjuger", "partiel"
            phrase += f"{contested} item(s) contesté(s) attendent l'atelier d'adjudication."
        else:
            badge, classe = "instrumenté · en cours", "pret"
            phrase += f"{validated} item(s) validé(s) sur {instr}."
        blocks.append(f"""    <div class="callout">
      <h3>{row['name']}</h3><span class="etat {classe}">{badge}</span>
      <p>{phrase}</p>
    </div>""")
    return "\n".join(blocks)


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

    campaigns = load_campaigns(current_catalog_sources({
        "LOTUSim_Mission_Catalog": mc_version,
        "LOTUSim_Task_Catalog": tc_version,
        "LOTUSim_Method_Catalog": tm_version,
    }))
    kpi = {key: sum(c[key] for c in campaigns)
           for key in ("instrumented", "exposed", "validated", "contested", "stale")}
    exp_total = kpi["instrumented"]
    exp_valides = kpi["validated"]

    referential_rows = [
        {"name": "Ontologie", "inventory": str(len(data.ontology)), "inventory_label": "classes",
         "prefix": "LOTUSim_Naval_Maritime_Ontology"},
        {"name": "Mission Catalog", "inventory": str(counts["missions"]),
         "inventory_label": f"missions · {candidates} candidates", "prefix": "LOTUSim_Mission_Catalog"},
        {"name": "Task Catalog", "inventory": str(counts["signatures"]),
         "inventory_label": "signatures", "prefix": "LOTUSim_Task_Catalog"},
        {"name": "State Model", "inventory": str(counts["states"]),
         "inventory_label": f"états · {counts['state_types']} types", "prefix": "LOTUSim_State_Model"},
        {"name": "Method Catalog", "inventory": str(counts["methods"]),
         "inventory_label": "méthodes pilotes", "prefix": "LOTUSim_Method_Catalog"},
    ]
    for row in referential_rows:
        row["campaigns"] = [c for c in campaigns if c["catalog_prefix"] == row["prefix"]]
        row["expert_review"] = {
            key: sum(c[key] for c in row["campaigns"])
            for key in ("instrumented", "exposed", "validated", "contested", "stale")
        } if row["campaigns"] else None
    orphans = [c["name"] for c in campaigns
               if c["catalog_prefix"] not in {r["prefix"] for r in referential_rows}]
    if orphans:
        fail(f"campaigns target unknown referentials: {orphans}")

    instrumented_rows = [r for r in referential_rows if r["campaigns"]]
    instrumented_names = ", ".join(r["name"] for r in instrumented_rows)
    mois = ["janvier", "février", "mars", "avril", "mai", "juin", "juillet",
            "août", "septembre", "octobre", "novembre", "décembre"]
    now = datetime.datetime.now(datetime.timezone.utc)

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
        "__DATE_COURTE__": f"{now.day} {mois[now.month - 1]} {now.year}",
        "__TUILE_REF_PCT__": str(pct(len(instrumented_rows), len(referential_rows))),
        "__TUILE_REF_NOTE__": f"{len(instrumented_rows)} sur {len(referential_rows)} : {instrumented_names}",
        "__TUILE_VAL_PCT__": str(pct(kpi["validated"], kpi["instrumented"])),
        "__TUILE_VAL_NOTE__": f"{kpi['validated']} sur {kpi['instrumented']} items, périmètre {instrumented_names}",
        "__TUILE_QUESTIONS__": str(sum(c["asked"] for c in campaigns)),
        "__TUILE_QUESTIONS_NOTE__": f"{kpi['instrumented'] - sum(c['asked'] for c in campaigns)} items supplémentaires dédupliqués",
        "__MATRICE_LIGNES__": matrix_rows(referential_rows),
        "__CALLOUTS__": callouts(referential_rows),
        "__CAMPAGNES_LIGNES__": campaign_rows(campaigns),
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
                               "abstract_covered": len(covered),
                               "expert_review": next(r["expert_review"] for r in referential_rows
                                                     if r["prefix"] == "LOTUSim_Method_Catalog")},
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
