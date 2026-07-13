# Update to DEM-1 — Semantic Design Rules

## Additional Rule

### SDR-11 — Common semantics shall be centralized

Common operational semantics shared by multiple tasks shall be defined once at the Semantic Family level within the Task Catalog.

Individual tasks shall only specify the semantic specialization required by their own signatures.

This rule minimizes duplication, guarantees consistency and simplifies derivation of the State Model.
