from pathlib import Path

from agentic_qa.retrieval.symbols.indexer import (
    PythonAstSymbolIndexer,
)


def main() -> None:
    repository_path = Path("sample_automation")

    indexer = PythonAstSymbolIndexer(
        repository_path=repository_path,
    )

    index = indexer.build_index()

    print(f"Repository: {repository_path}")
    print(f"Total symbols: {len(index.symbols)}")
    print()

    for symbol in index.symbols:
        print(
            f"{symbol.symbol_type.value.upper():<10} "
            f"{symbol.qualified_name:<45} "
            f"{symbol.path}:"
            f"{symbol.start_line}-{symbol.end_line}"
        )

        if symbol.parameters:
            print(" " * 12 + "parameters: " + ", ".join(symbol.parameters))

        if symbol.decorators:
            print(" " * 12 + "decorators: " + ", ".join(symbol.decorators))

        if symbol.bases:
            print(" " * 12 + "bases: " + ", ".join(symbol.bases))

        print()


if __name__ == "__main__":
    main()
