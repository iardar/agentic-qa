# Agentic QA | Evaluation Documentation Update (18 October 2026)

## Documentation update | 18 October 2026

STATUS: The original handbook chapters are preserved as historical milestones. This revision supersedes older “current” claims about 7-case retrieval baselines and the V2 retriever being planned. All results below are from the two user-provided LangSmith CSV exports; no new LangSmith evaluation was executed during this update.

## Current workflow and scope

Requirement -> analyze_requirement -> retrieve_context -> inspect_symbols (planned/partly independent) -> explore_ui (MCP integration planned) -> design_test -> generate_test -> run_test -> analyze_result -> review/repair. The actively evaluated retrieval strategies are V1.2 token-aware file retrieval and V2.0 AST symbol retrieval followed by unique-file projection. V2.1 dependency expansion is proposed, not implemented.

## Repository retrieval datasets

repository-retrieval-realworld-v1: frozen 7-case benchmark (4 auth, 3 article). repository-retrieval-realworld-v2: 10-case benchmark (4 auth, 3 article, 3 comment), run on the expanded sample_automation corpus. Historic v1 experiments must be retained; comparisons between algorithm versions should use the same dataset version and repository revision.

## V2.0 retrieval implementation

PythonAstSymbolIndexer produces RepositorySymbolIndex. SymbolRepositoryContextProvider ranks individual symbols using exact token matches in names, parameters, parent/path and source. project_symbols_to_repository_context deduplicates ranked symbols into a RepositoryContext of unique file paths (top 8). V1.2 remains token-aware whole-file keyword retrieval. Neither retriever currently performs relationship-driven fixture/import dependency expansion.

## LangSmith evaluation v2 | measured macro averages

Metric | V1.2 | V2.0 | Difference (percentage points): precision_at_3: 46.7% -> 50.0% (+3.3 pp); recall_at_3: 33.7% -> 35.3% (+1.6 pp); recall_at_5: 45.5% -> 49.8% (+4.3 pp); top1_relevant: 80.0% -> 100.0% (+20.0 pp). All 10 cases completed in both exports. Top1 improves markedly; recall remains moderate.

## Per-case Recall@5

Edit article: V1.2 60% / V2.0 40%; Delete own comment: V1.2 17% / V2.0 33%; View existing comment: V1.2 20% / V2.0 20%; Delete article: V1.2 40% / V2.0 20%; Register a new user: V1.2 50% / V2.0 50%; Sign in with registered credentials: V1.2 25% / V2.0 75%; Attempt to sign up with a valid email and password while leaving the username empty: V1.2 100% / V2.0 67%; Create comment: V1.2 17% / V2.0 33%; Create article: V1.2 60% / V2.0 60%; Sign in with a valid registered email and an invalid password: V1.2 67% / V2.0 100%

## Interpretation and limitation

V2.0 improves primary-artifact identification (Top1: 80% to 100%) with limited improvement in context completeness (Recall@5: 45.5% to 49.8%). Ranked results are often dominated by similar test files instead of fixtures, API client, Page Objects, and data builders. In Delete Comment, V2.0 returns only two of six required artifacts by rank 8: the test and comments fixture; the Page Object, Comment component, API client, and builder are absent. This supports evaluating dependency-aware expansion, not blindly changing weights. A 10-case benchmark is small and includes existing tests whose names echo requirements; results do not establish generalization to unseen behaviors.

## V2.1 plan and evaluation contract

PROPOSED, not implemented: start from top ranked tests/symbols; inspect pytest fixture parameters, local imports and Page Object/component references; resolve exact symbol definitions with AST; add limited one-hop related artifacts; project to deduplicated files. Evaluate V2.1 against frozen v2 dataset and same corpus; retain Top1 while improving Recall@3/5/8, monitor precision and failure cases. Do not modify V1.2 or V2.0 during the comparison.

## Reproducibility and snapshot discrepancy

Current user-reported LangSmith runs targeted repository-retrieval-realworld-v2. The attached agentic-qa(2).zip snapshot still contains scripts pointing to repository-retrieval-realworld-v1 and an empty comments.py evaluation list. Treat this as a snapshot mismatch: the successful v2 experiments and CSV exports evidence newer local changes not included in that archive. Synchronize a committed repository state before any future rerun; do not claim the archive itself contains the 10-case dataset source.

## Quality safeguards

Run ruff, mypy and pytest; keep fixture setup/cleanup API-backed and browser behavior UI-backed. In single-script mypy invocations, ensure the local src/ package is discoverable and typed (py.typed if distributing as PEP 561 typed package). Do not confuse mypy packaging problems with retrieval evaluation regressions. Preserve failing test evidence before any repair.

## Evidence

Sources: 10-row CSV files realworld-dataset-v2-retrieval-v1.2-token-aware-48b9dd6a.csv and realworld-datadset-v2-retrieval-v2.0-symbol-token-aware-94cb88d6.csv; repository snapshot agentic-qa(2).zip; historical docs/ handbooks. Numbers are macro averages of exported feedback scores.

