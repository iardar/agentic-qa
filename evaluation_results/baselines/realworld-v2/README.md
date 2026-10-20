# RealWorld Retrieval Benchmark V2 — Frozen Baseline

**Dataset:** `repository-retrieval-realworld-v2`

**Evaluation cases:** 10

**Retrieval implementations:**
- V1.2 — token-aware file retrieval
- V2.0 — AST symbol-level retrieval

## Results

| Metric | V1.2 | V2.0 |
|---|---:|---:|
| Precision@3 | 0.467 | 0.500 |
| Recall@3 | 0.337 | 0.353 |
| Recall@5 | 0.455 | 0.498 |
| Top1 relevant | 0.800 | 1.000 |
| Recall@8 | 0.713 | 0.662 |

Values are rounded macro averages.

## Experiment rules

- Do not modify the frozen V1.2 or V2.0 retrieval algorithms.
- Do not modify or append examples to the v2 LangSmith dataset.
- Preserve the original 10 evaluation cases and their expected paths.
- Run future retrieval versions against the same frozen repository corpus and dataset for direct comparison.
- Use a new dataset version when the corpus or ground-truth cases change.

## Baseline conclusion

V2.0 improves primary-artifact identification but does not retrieve sufficiently complete supporting repository context.

The next experiment, V2.1, will investigate dependency-aware expansion.

## Provenance

Record the Git commit SHA, LangSmith dataset ID, experiment IDs, and experiment dates here before creating the baseline tag.

84dfff320ae86c67af4c17292404ec755910924e