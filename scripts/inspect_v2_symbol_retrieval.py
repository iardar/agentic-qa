from pathlib import Path

from agentic_qa.evals.retrieval.cases.realworld import (
    REAL_WORLD_CASES,
)
from agentic_qa.evals.retrieval.evaluator import (
    calculate_retrieval_metrics,
)
from agentic_qa.retrieval.symbols.indexer import (
    PythonAstSymbolIndexer,
)
from agentic_qa.retrieval.symbols.projection import (
    project_symbols_to_repository_context,
)
from agentic_qa.retrieval.symbols.provider import (
    SymbolRepositoryContextProvider,
)

REPOSITORY_PATH = Path("sample_automation")

TOP_K_SYMBOLS = 50
TOP_K_FILES = 8

SYMBOL_PREVIEW_LIMIT = 10


def main() -> None:
    indexer = PythonAstSymbolIndexer(
        repository_path=REPOSITORY_PATH,
    )

    symbol_index = indexer.build_index()

    provider = SymbolRepositoryContextProvider(
        symbol_index=symbol_index,
        top_k_symbols=TOP_K_SYMBOLS,
    )

    print(f"Repository: {REPOSITORY_PATH}")
    print(f"Indexed symbols: {len(symbol_index.symbols)}")
    print(f"Evaluation cases: {len(REAL_WORLD_CASES)}")

    all_metrics = []

    for case in REAL_WORLD_CASES:
        symbol_context = provider.retrieve(
            case.analysis,
        )

        repository_context = (
            project_symbols_to_repository_context(
                symbol_context,
                top_k=TOP_K_FILES,
            )
        )

        required_paths = set(case.required_paths)

        print()
        print("=" * 100)
        print(f"CASE: {case.name}")
        print("=" * 100)

        print()
        print("QUERY TERMS:")
        print(symbol_context.query_terms)

        print()
        print("REQUIRED PATHS:")

        for path in case.required_paths:
            print(f"  {path}")

        print()
        print("TOP SYMBOLS:")

        for rank, item in enumerate(
            symbol_context.items[:SYMBOL_PREVIEW_LIMIT],
            start=1,
        ):
            symbol = item.symbol

            required_marker = (
                "[REQ]"
                if symbol.path in required_paths
                else "     "
            )

            print(
                f"{rank:>2}. "
                f"{required_marker} "
                f"{symbol.symbol_type.value.upper():<8} "
                f"{symbol.qualified_name}"
            )

            print(
                f"     score={item.score} "
                f"path={symbol.path}"
            )

            print(
                f"     matched={item.matched_terms}"
            )

        first_symbol_by_path: dict[str, str] = {}

        for item in symbol_context.items:
            first_symbol_by_path.setdefault(
                item.symbol.path,
                item.symbol.qualified_name,
            )

        print()
        print("PROJECTED FILES:")

        for rank, item in enumerate(
            repository_context.items,
            start=1,
        ):
            required_marker = (
                "[REQ]"
                if item.path in required_paths
                else "     "
            )

            origin_symbol = first_symbol_by_path[
                item.path
            ]

            print(
                f"{rank:>2}. "
                f"{required_marker} "
                f"{item.path}"
            )

            print(
                f"     score={item.score} "
                f"via={origin_symbol}"
            )

        metrics = calculate_retrieval_metrics(
            context=repository_context,
            required_paths=case.required_paths,
        )

        all_metrics.append(metrics)

        print()
        print("METRICS:")
        print(
            f"  Top1 Relevant : "
            f"{int(metrics.top1_relevant)}"
        )
        print(
            f"  Precision@3   : "
            f"{metrics.precision_at_3:.2f}"
        )
        print(
            f"  Recall@3      : "
            f"{metrics.recall_at_3:.2f}"
        )
        print(
            f"  Recall@5      : "
            f"{metrics.recall_at_5:.2f}"
        )

    case_count = len(all_metrics)

    if case_count == 0:
        return

    average_top1 = (
        sum(
            int(metrics.top1_relevant)
            for metrics in all_metrics
        )
        / case_count
    )

    average_precision_at_3 = (
        sum(
            metrics.precision_at_3
            for metrics in all_metrics
        )
        / case_count
    )

    average_recall_at_3 = (
        sum(
            metrics.recall_at_3
            for metrics in all_metrics
        )
        / case_count
    )

    average_recall_at_5 = (
        sum(
            metrics.recall_at_5
            for metrics in all_metrics
        )
        / case_count
    )

    print()
    print("=" * 100)
    print("V2 LOCAL AGGREGATE")
    print("=" * 100)
    print(f"Cases       : {case_count}")
    print(f"Top1        : {average_top1:.2f}")
    print(
        f"Precision@3 : "
        f"{average_precision_at_3:.2f}"
    )
    print(
        f"Recall@3    : "
        f"{average_recall_at_3:.2f}"
    )
    print(
        f"Recall@5    : "
        f"{average_recall_at_5:.2f}"
    )


if __name__ == "__main__":
    main()