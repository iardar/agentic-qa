import re
from collections import Counter

from agentic_qa.models import RequirementAnalysis
from agentic_qa.retrieval.symbols.models import (
    RepositorySymbol,
    RepositorySymbolIndex,
    RetrievedSymbol,
    SymbolRetrievalContext,
)


def _tokenize_symbol_text(text: str) -> list[str]:
    """Split prose and Python identifiers into normalized tokens."""

    normalized = text.replace("_", " ")

    normalized = re.sub(
        r"(?<=[a-z0-9])(?=[A-Z])",
        " ",
        normalized,
    )

    return re.findall(
        r"[A-Za-z0-9]+",
        normalized.lower(),
    )


class SymbolRepositoryContextProvider:
    STOP_WORDS = {
        "the",
        "and",
        "for",
        "with",
        "when",
        "that",
        "this",
        "should",
        "user",
        "users",
        "verify",
        "able",
        "from",
        "into",
        "after",
        "before",
        "then",
        "their",
        "they",
        "them",
        "can",
        "has",
        "using",
        "successfully",
        "application",
        "page",
    }

    def __init__(
        self,
        symbol_index: RepositorySymbolIndex,
        top_k_symbols: int = 50,
    ) -> None:
        if top_k_symbols <= 0:
            raise ValueError(
                "top_k_symbols must be greater than zero."
            )

        self._symbol_index = symbol_index
        self._top_k_symbols = top_k_symbols

    def retrieve(
        self,
        analysis: RequirementAnalysis,
    ) -> SymbolRetrievalContext:
        query_terms = self._build_query_terms(analysis)

        candidates: list[RetrievedSymbol] = []

        for symbol in self._symbol_index.symbols:
            item = self._score_symbol(
                symbol=symbol,
                query_terms=query_terms,
            )

            if item is not None:
                candidates.append(item)

        candidates.sort(
            key=lambda item: (
                -item.score,
                item.symbol.path,
                item.symbol.qualified_name,
            )
        )

        return SymbolRetrievalContext(
            query_terms=query_terms,
            items=candidates[: self._top_k_symbols],
        )

    def _build_query_terms(
        self,
        analysis: RequirementAnalysis,
    ) -> list[str]:
        values = [
            analysis.feature,
            analysis.operation,
            *analysis.conditions,
            *analysis.expected_outcomes,
        ]

        text = " ".join(values)

        words = re.findall(
            r"[A-Za-z0-9_]+",
            text.lower(),
        )

        terms = {
            word
            for word in words
            if (
                len(word) >= 3
                and word not in self.STOP_WORDS
            )
        }

        return sorted(terms)

    def _score_symbol(
        self,
        symbol: RepositorySymbol,
        query_terms: list[str],
    ) -> RetrievedSymbol | None:
        qualified_name_tokens = set(
            _tokenize_symbol_text(
                symbol.qualified_name
            )
        )

        parameter_tokens = set(
            _tokenize_symbol_text(
                " ".join(symbol.parameters)
            )
        )

        parent_tokens = set(
            _tokenize_symbol_text(
                symbol.parent or ""
            )
        )

        path_tokens = set(
            _tokenize_symbol_text(
                symbol.path
            )
        )

        source_tokens = Counter(
            _tokenize_symbol_text(
                symbol.source
            )
        )

        score = 0.0
        matched_terms: list[str] = []

        for term in query_terms:
            term_score = 0.0

            if term in qualified_name_tokens:
                term_score += 8.0

            if term in parameter_tokens:
                term_score += 4.0

            if term in parent_tokens:
                term_score += 3.0

            if term in path_tokens:
                term_score += 3.0

            occurrences = source_tokens[term]

            if occurrences > 0:
                term_score += min(
                    float(occurrences),
                    3.0,
                )

            if term_score > 0:
                matched_terms.append(term)
                score += term_score

        if score == 0:
            return None

        return RetrievedSymbol(
            symbol=symbol,
            score=score,
            matched_terms=matched_terms,
        )