#!/usr/bin/env python3
"""Generate the expert-review item matrix and questionnaire from the Method Catalog.

The generator walks every concrete method of the Method Catalog and derives one
verification item per doctrinal decision (applicability condition, capability
requirement, decomposition, ordering, synchronization, completion criteria,
failure propagation, type narrowing), plus signature-level items (missing
applicability condition, missing alternative method) and catalog-level items
declared in the wording file (method-choice scenarios).

Coverage is structural: an item exists for every relevant field of every
method, whether or not a wording exists. Items whose semantic fingerprint
already appeared in a previous method are marked `covered_by` and not asked
again. Every remaining item must have a French wording, otherwise generation
fails: an unworded item is an unverifiable doctrinal decision.

Outputs (under validation/expert-review/):
- items_<campaign>.yaml   : full coverage matrix with per-item review status;
- questionnaire_<campaign>.html : self-contained offline questionnaire.

Usage:
    python tools/validation/generate_expert_review.py \
        --wording validation/expert-review/wording_escort_v0.1.yaml
"""

from __future__ import annotations

import argparse
import datetime
import hashlib
import json
import re
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[2]
DEFAULT_CATALOG = ROOT / "references" / "method-catalog" / "LOTUSim_Method_Catalog_v0.2.0.md"
OUTPUT_DIR = ROOT / "validation" / "expert-review"

METHOD_ID_RE = re.compile(r"TM-\d{3}-S\d{2}-M\d{2}")
CAPABILITY_STATE = "SM-ST-010"


def workspace_path(path: Path, label: str) -> Path:
    resolved = path.resolve()
    try:
        resolved.relative_to(ROOT.resolve())
    except ValueError as exc:
        raise ValueError(f"{label} must stay inside the repository: {resolved}") from exc
    return resolved


def load_methods(catalog_path: Path) -> list[dict]:
    text = catalog_path.read_text(encoding="utf-8")
    methods = []
    for block in re.findall(r"```yaml\n(.*?)```", text, re.S):
        try:
            data = yaml.safe_load(block)
        except yaml.YAMLError:
            continue
        if isinstance(data, dict) and METHOD_ID_RE.fullmatch(str(data.get("id", ""))):
            methods.append(data)
    return methods


def short(method_id: str) -> str:
    return method_id  # full ids keep items unambiguous across future signatures


def cap_entry(entry: dict) -> tuple[str, str]:
    bindings = entry.get("bindings", {})
    return (str(bindings.get("entity", "?")), str(bindings.get("capability", "?")))


def build_method_items(method: dict) -> list[dict]:
    mid = method["id"]
    items: list[dict] = []

    def add(item_id: str, category: str, targets: list, fingerprint) -> None:
        items.append({
            "id": item_id,
            "scope": "method",
            "method": mid,
            "category": category,
            "targets": targets,
            "fingerprint": repr((category, fingerprint)),
        })

    capabilities = []
    for entry in method.get("applicability", []):
        ref = entry.get("state_ref", "?")
        if ref == CAPABILITY_STATE:
            capabilities.append(entry)
        else:
            add(f"VQ-{mid}-APP-{ref.replace('SM-ST-', 'ST')}", "applicability",
                [entry], ref)
    if capabilities:
        caps = sorted(cap_entry(e) for e in capabilities)
        add(f"VQ-{mid}-CAP", "capabilities", capabilities, tuple(caps))

    network = method.get("task_network", {})
    subtask_refs = sorted(str(s.get("task_ref")) for s in network.get("subtasks", []))
    add(f"VQ-{mid}-DEC", "decomposition", network.get("subtasks", []), tuple(subtask_refs))
    add(f"VQ-{mid}-ORD", "ordering", network.get("ordering", []),
        tuple(sorted(map(repr, network.get("ordering", [])))))
    sync = network.get("synchronization", [])
    if sync:
        add(f"VQ-{mid}-SYNC", "synchronization", sync,
            tuple(sorted(str(s.get("relation")) for s in sync)))

    completion = method.get("completion_support", [])
    if completion:
        add(f"VQ-{mid}-COMP", "completion", completion,
            tuple(sorted(str(c.get("state_ref")) for c in completion)))

    for entry in method.get("failure_propagation", []):
        origin = str(entry.get("from", "?"))
        outcome = origin.split(".", 1)[-1]
        response = str(entry.get("decision") or entry.get("parent_outcome") or "?")
        add(f"VQ-{mid}-FAIL-{outcome}", "failure", [entry], (outcome, response))

    inherited = [p for p in method.get("parameters", [])
                 if p.get("source", {}).get("kind") == "parent_task"]
    if inherited:
        narrowing = sorted((str(p.get("role")), str(p.get("type"))) for p in inherited)
        add(f"VQ-{mid}-NARROW", "type_narrowing", inherited, tuple(narrowing))

    return items


def build_signature_items(methods: list[dict]) -> list[dict]:
    items = []
    by_signature: dict[str, list[dict]] = {}
    for method in methods:
        by_signature.setdefault(str(method.get("decomposes")), []).append(method)
    for signature, sig_methods in sorted(by_signature.items()):
        items.append({
            "id": f"VQ-{signature}-SIG-APPGAP",
            "scope": "signature",
            "signature": signature,
            "category": "applicability_gap",
            "targets": [m["id"] for m in sig_methods],
            "fingerprint": repr(("applicability_gap", signature)),
        })
        items.append({
            "id": f"VQ-{signature}-SIG-ALTGAP",
            "scope": "signature",
            "signature": signature,
            "category": "alternative_gap",
            "targets": [m["id"] for m in sig_methods],
            "fingerprint": repr(("alternative_gap", signature)),
        })
        if len(sig_methods) > 1:
            items.append({
                "id": f"VQ-{signature}-SIG-DISCRIM",
                "scope": "signature",
                "signature": signature,
                "category": "discriminant",
                "targets": [m["id"] for m in sig_methods],
                "fingerprint": repr(("discriminant", signature)),
            })
    return items


def deduplicate(items: list[dict]) -> None:
    seen: dict[str, str] = {}
    for item in items:
        fingerprint = item["fingerprint"]
        if fingerprint in seen:
            item["covered_by"] = seen[fingerprint]
        else:
            seen[fingerprint] = item["id"]


def merge_wording(items: list[dict], wording: dict) -> list[str]:
    worded = {w["id"]: w for w in wording.get("items", [])}
    errors = []
    for item in items:
        if "covered_by" in item:
            continue
        entry = worded.pop(item["id"], None)
        if entry is None:
            errors.append(f"item sans formulation : {item['id']} ({item['category']})")
            continue
        item["question"] = {k: v for k, v in entry.items() if k != "id"}
    for extra_id, entry in worded.items():
        if entry.get("scope") == "catalog":
            items.append({
                "id": extra_id,
                "scope": "catalog",
                "category": entry.get("category", "method_choice"),
                "targets": entry.get("targets", []),
                "question": {k: v for k, v in entry.items()
                             if k not in ("id", "scope", "targets", "category")},
            })
        else:
            errors.append(f"formulation orpheline (aucun item généré) : {extra_id}")
    return errors


HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="utf-8">
<title>__TITLE__</title>
<style>
  body { font-family: "Segoe UI", system-ui, sans-serif; margin: 0; background: #f2f4f7; color: #1c2733; }
  .wrap { max-width: 780px; margin: 0 auto; padding: 24px 16px 80px; }
  h1 { font-size: 1.35rem; margin: 0 0 4px; }
  .meta { color: #5b6b7b; font-size: 0.9rem; margin-bottom: 18px; }
  .card { background: #fff; border: 1px solid #dde3ea; border-radius: 10px; padding: 18px 20px; margin-bottom: 14px; }
  .scenario { background: #eef4fb; border: 1px solid #c9dcf0; border-radius: 10px; padding: 14px 18px; margin-bottom: 18px; font-size: 0.95rem; }
  .tag { display: inline-block; font-size: 0.72rem; letter-spacing: 0.04em; text-transform: uppercase; color: #4c6ef5; background: #edf1ff; border-radius: 4px; padding: 2px 8px; margin-bottom: 8px; }
  .statement { font-size: 1rem; line-height: 1.5; margin: 0 0 12px; }
  .choices { display: flex; gap: 8px; flex-wrap: wrap; }
  .choices label { border: 1px solid #c6cfd9; border-radius: 8px; padding: 8px 14px; cursor: pointer; user-select: none; background: #fafbfc; }
  .choices input { margin-right: 6px; }
  .choices label:has(input:checked) { border-color: #4c6ef5; background: #edf1ff; font-weight: 600; }
  textarea { width: 100%; box-sizing: border-box; min-height: 64px; margin-top: 10px; border: 1px solid #c6cfd9; border-radius: 8px; padding: 8px; font: inherit; }
  .hint { font-size: 0.82rem; color: #8a5a00; margin-top: 6px; display: none; }
  .progress { position: fixed; bottom: 0; left: 0; right: 0; background: #fff; border-top: 1px solid #dde3ea; padding: 10px 16px; display: flex; align-items: center; gap: 14px; }
  .bar { flex: 1; height: 8px; background: #e3e8ee; border-radius: 4px; overflow: hidden; }
  .bar > div { height: 100%; width: 0; background: #4c6ef5; transition: width 0.2s; }
  button { background: #4c6ef5; color: #fff; border: 0; border-radius: 8px; padding: 10px 18px; font: inherit; font-weight: 600; cursor: pointer; }
  button:disabled { background: #aab6c6; cursor: not-allowed; }
  input[type=text] { border: 1px solid #c6cfd9; border-radius: 8px; padding: 8px; font: inherit; width: 100%; box-sizing: border-box; }
  .idline { font-size: 0.72rem; color: #9aa7b4; margin-top: 10px; }
</style>
</head>
<body>
<div class="wrap">
  <h1>__TITLE__</h1>
  <div class="meta">Campagne __CAMPAIGN__ — générée le __DATE__ depuis le Method Catalog __CATALOG_VERSION__.
  Vos réponses restent locales : rien n'est transmis tant que vous n'exportez pas le fichier.</div>
  <div class="card">
    <div class="tag">Relecteur</div>
    <p class="statement">Votre nom (ou trigramme) :</p>
    <input type="text" id="expert" placeholder="ex. E. Chauveau">
    <p class="statement" style="margin-top:12px">Répondez d'après votre expérience opérationnelle, pas d'après ce que le modèle « devrait » dire.
    <strong>« Ça dépend » est une réponse précieuse</strong> : elle doit être accompagnée d'un commentaire expliquant de quoi ça dépend.</p>
  </div>
  <div class="scenario">__INTRO__</div>
  <div id="questions"></div>
  <div class="progress">
    <div class="bar"><div id="fill"></div></div>
    <span id="count">0 / 0</span>
    <button id="export" disabled>Exporter mes réponses</button>
  </div>
</div>
<script>
const ITEMS = __ITEMS_JSON__;
const answers = {};
const container = document.getElementById("questions");

function render() {
  ITEMS.forEach((it, idx) => {
    const card = document.createElement("div");
    card.className = "card";
    const q = it.question;
    let choicesHtml = "";
    if (q.format === "vf") {
      choicesHtml = ["Vrai", "Faux", "Ça dépend"].map(v =>
        `<label><input type="radio" name="${it.id}" value="${v}">${v}</label>`).join("");
    } else if (q.format === "choice") {
      choicesHtml = q.options.map(v =>
        `<label><input type="radio" name="${it.id}" value="${v}">${v}</label>`).join("");
    }
    card.innerHTML = `
      <div class="tag">${idx + 1}. ${q.theme || it.category}</div>
      ${q.context ? `<p class="statement" style="color:#5b6b7b">${q.context}</p>` : ""}
      <p class="statement">${q.statement}</p>
      <div class="choices">${choicesHtml}</div>
      <textarea placeholder="${q.format === "open" ? "Votre réponse…" : "Commentaire (obligatoire si « Ça dépend »)…"}"></textarea>
      <div class="hint">Merci de préciser de quoi ça dépend.</div>
      <div class="idline">${it.id}</div>`;
    container.appendChild(card);
    const update = () => {
      const chosen = card.querySelector("input:checked");
      const comment = card.querySelector("textarea").value.trim();
      const hint = card.querySelector(".hint");
      let done = false;
      if (q.format === "open") { done = comment.length > 0; }
      else if (chosen) {
        const needsComment = chosen.value === "Ça dépend";
        hint.style.display = needsComment && !comment ? "block" : "none";
        done = !needsComment || comment.length > 0;
      }
      if (done) { answers[it.id] = { value: chosen ? chosen.value : null, comment: comment }; }
      else { delete answers[it.id]; }
      refresh();
    };
    card.addEventListener("change", update);
    card.querySelector("textarea").addEventListener("input", update);
  });
  refresh();
}

function refresh() {
  const total = ITEMS.length;
  const done = Object.keys(answers).length;
  document.getElementById("count").textContent = done + " / " + total;
  document.getElementById("fill").style.width = (100 * done / total) + "%";
  document.getElementById("export").disabled = done < total || !document.getElementById("expert").value.trim();
}
document.getElementById("expert").addEventListener("input", refresh);

document.getElementById("export").addEventListener("click", () => {
  const expert = document.getElementById("expert").value.trim();
  const payload = {
    campaign: "__CAMPAIGN__",
    catalog_version: "__CATALOG_VERSION__",
    expert: expert,
    exported_at: new Date().toISOString(),
    answers: answers
  };
  const blob = new Blob([JSON.stringify(payload, null, 2)], { type: "application/json" });
  const a = document.createElement("a");
  a.href = URL.createObjectURL(blob);
  a.download = "reponses___CAMPAIGN___" + expert.replace(/\\W+/g, "-") + ".json";
  a.click();
});
render();
</script>
</body>
</html>
"""


def render_html(items: list[dict], wording: dict, catalog_version: str) -> str:
    asked = [i for i in items if "covered_by" not in i]
    # `expected` and analyst notes must never reach the experts: the review is blind.
    payload = [{"id": i["id"], "category": i["category"],
                "question": {k: v for k, v in i["question"].items()
                             if k not in ("expected", "note_analyste")}}
               for i in asked]
    html = HTML_TEMPLATE
    html = html.replace("__TITLE__", wording.get("title", "Revue experte"))
    html = html.replace("__CAMPAIGN__", wording.get("campaign", "campagne"))
    html = html.replace("__INTRO__", wording.get("scenario_intro", "").replace("\n", "<br>"))
    html = html.replace("__DATE__", datetime.date.today().isoformat())
    html = html.replace("__CATALOG_VERSION__", catalog_version)
    html = html.replace("__ITEMS_JSON__", json.dumps(payload, ensure_ascii=False, indent=1))
    return html


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--catalog", type=Path, default=DEFAULT_CATALOG)
    parser.add_argument("--wording", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, default=OUTPUT_DIR)
    args = parser.parse_args()
    try:
        args.catalog = workspace_path(args.catalog, "catalog")
        args.wording = workspace_path(args.wording, "wording")
        args.output_dir = workspace_path(args.output_dir, "output directory")
    except ValueError as exc:
        print(f"Generation refused: {exc}", file=sys.stderr)
        return 1

    methods = load_methods(args.catalog)
    if not methods:
        print("Aucune méthode concrète trouvée dans le catalogue.", file=sys.stderr)
        return 1
    wording = yaml.safe_load(args.wording.read_text(encoding="utf-8"))
    campaign = wording.get("campaign", "campagne")

    items: list[dict] = []
    for method in methods:
        items.extend(build_method_items(method))
    items.extend(build_signature_items(methods))
    deduplicate(items)
    errors = merge_wording(items, wording)
    if errors:
        print("Génération refusée : la couverture n'est pas complète.", file=sys.stderr)
        for error in errors:
            print(" -", error, file=sys.stderr)
        return 1

    catalog_match = re.search(r"\*\*Version:\*\*\s*([\d.]+)",
                              args.catalog.read_text(encoding="utf-8"))
    catalog_version = catalog_match.group(1) if catalog_match else "?"

    args.output_dir.mkdir(parents=True, exist_ok=True)
    matrix = {
        "campaign": campaign,
        "generated": datetime.date.today().isoformat(),
        "catalog": args.catalog.name,
        "catalog_version": catalog_version,
        "catalog_sha256": hashlib.sha256(args.catalog.read_bytes()).hexdigest(),
        "review_rule": "un item est `validé` après accord d'au moins un expert ; "
                       "toute réponse « Ça dépend » ou divergente passe l'item en `contesté`",
        "items": [
            {k: v for k, v in item.items() if k != "fingerprint"} | {"status": "pending"}
            for item in items
        ],
    }
    items_path = args.output_dir / f"items_{campaign}.yaml"
    items_path.write_text(yaml.safe_dump(matrix, allow_unicode=True, sort_keys=False,
                                         width=100), encoding="utf-8")

    html_path = args.output_dir / f"questionnaire_{campaign}.html"
    html_path.write_text(render_html(items, wording, catalog_version), encoding="utf-8")

    asked = sum(1 for i in items if "covered_by" not in i)
    deduped = sum(1 for i in items if "covered_by" in i)
    print(f"{len(items)} items générés ({asked} questions posées, {deduped} couverts par dédoublonnage).")
    print(f"Matrice  : {items_path.relative_to(ROOT)}")
    print(f"Formulaire : {html_path.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
