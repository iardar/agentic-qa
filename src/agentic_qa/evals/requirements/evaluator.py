from dataclasses import dataclass

from agentic_qa.evals.requirements.cases import (
    RequirementEvaluationCase,
)
from agentic_qa.models import RequirementAnalysis


@dataclass
class CheckResult:
    name: str
    passed: bool
    message: str


def contains_terms(
    values: list[str],
    terms: list[str],
) -> bool:
    text = " ".join(values).lower()

    return all(
        term.lower() in text
        for term in terms
    )


def contains_alternatives(
    values: list[str],
    alternatives: list[list[str]],
) -> bool:
    text = " ".join(values).lower()

    return all(
        any(
            alternative.lower() in text
            for alternative in group
        )
        for group in alternatives
    )


def evaluate_analysis(
    analysis: RequirementAnalysis,
    case: RequirementEvaluationCase,
) -> list[CheckResult]:
    results: list[CheckResult] = []

    results.append(
        CheckResult(
            name="interaction_surface",
            passed=(
                analysis.interaction_surface
                == case.expected_surface
            ),
            message=(
                f"expected={case.expected_surface.value}, "
                f"actual={analysis.interaction_surface.value}"
            ),
        )
    )

    if case.required_condition_terms:
        results.append(
            CheckResult(
                name="condition_terms",
                passed=contains_terms(
                    analysis.conditions,
                    case.required_condition_terms,
                ),
                message=(
                    "required terms="
                    f"{case.required_condition_terms}"
                ),
            )
        )

    if case.required_condition_alternatives:
        results.append(
            CheckResult(
                name="condition_concepts",
                passed=contains_alternatives(
                    analysis.conditions,
                    case.required_condition_alternatives,
                ),
                message=(
                    "accepted alternatives="
                    f"{case.required_condition_alternatives}"
                ),
            )
        )

    if case.required_outcome_terms:
        results.append(
            CheckResult(
                name="outcome_terms",
                passed=contains_terms(
                    analysis.expected_outcomes,
                    case.required_outcome_terms,
                ),
                message=(
                    "required terms="
                    f"{case.required_outcome_terms}"
                ),
            )
        )

    if case.required_outcome_alternatives:
        results.append(
            CheckResult(
                name="outcome_concepts",
                passed=contains_alternatives(
                    analysis.expected_outcomes,
                    case.required_outcome_alternatives,
                ),
                message=(
                    "accepted alternatives="
                    f"{case.required_outcome_alternatives}"
                ),
            )
        )

    if case.require_ambiguities is not None:
        has_ambiguities = bool(
            analysis.ambiguities
        )

        results.append(
            CheckResult(
                name="ambiguities",
                passed=(
                    has_ambiguities
                    == case.require_ambiguities
                ),
                message=(
                    "expected ambiguities="
                    f"{case.require_ambiguities}, "
                    "actual count="
                    f"{len(analysis.ambiguities)}"
                ),
            )
        )

    return results