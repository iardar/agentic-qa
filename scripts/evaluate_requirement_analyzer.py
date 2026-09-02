import json
from dataclasses import dataclass

from langchain_openai import ChatOpenAI

from agentic_qa.config import settings
from agentic_qa.models import RequirementAnalysis
from agentic_qa.requirements.llm_analyzer import (
    LLMRequirementAnalyzer,
)
from agentic_qa.evals.requirements.cases import (
    CASES,
    RequirementEvaluationCase,
)


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

def evaluate_case(
    case: RequirementEvaluationCase,
    analysis: RequirementAnalysis,
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
                    f"required terms="
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
                    f"accepted alternatives="
                    f"{case.required_condition_alternatives}"
                ),
            )
        )

    if case.required_outcome_terms:
        passed = contains_terms(
            analysis.expected_outcomes,
            case.required_outcome_terms,
        )

        results.append(
            CheckResult(
                name="outcome_terms",
                passed=passed,
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
                    f"expected ambiguities="
                    f"{case.require_ambiguities}, "
                    f"actual count="
                    f"{len(analysis.ambiguities)}"
                ),
            )
        )

    return results


def main() -> None:
    if settings.openai_api_key is None:
        raise RuntimeError(
            "OPENAI_API_KEY is not configured."
        )

    if not settings.llm_model:
        raise RuntimeError(
            "LLM_MODEL is not configured."
        )

    model = ChatOpenAI(
        model=settings.llm_model,
        api_key=(
            settings.openai_api_key
            .get_secret_value()
        ),
    )

    analyzer = LLMRequirementAnalyzer(
        model=model
    )

    total_checks = 0
    passed_checks = 0

    machine_results = []

    print(
        f"MODEL: {settings.llm_model}"
    )
    print()

    for case in CASES:
        print("=" * 80)
        print(f"CASE: {case.name}")
        print()

        analysis = analyzer.analyze(
            case.requirement
        )

        checks = evaluate_case(
            case,
            analysis,
        )

        print("REQUIREMENT:")
        print(case.requirement)
        print()

        print("ANALYSIS:")
        print(
            analysis.model_dump_json(
                indent=2
            )
        )

        print()
        print("CHECKS:")

        for check in checks:
            total_checks += 1

            if check.passed:
                passed_checks += 1
                status = "PASS"
            else:
                status = "FAIL"

            print(
                f"  {status:<4} "
                f"{check.name:<24} "
                f"{check.message}"
            )

        machine_results.append(
            {
                "case": case.name,
                "requirement": case.requirement,
                "analysis": (
                    analysis.model_dump(
                        mode="json"
                    )
                ),
                "checks": [
                    {
                        "name": check.name,
                        "passed": check.passed,
                        "message": check.message,
                    }
                    for check in checks
                ],
            }
        )

        print()

    score = (
        passed_checks / total_checks
        if total_checks
        else 0
    )

    print("=" * 80)
    print("SUMMARY")
    print()
    print(
        f"Passed: {passed_checks}/{total_checks}"
    )
    print(
        f"Score:  {score:.1%}"
    )

    with open(
        "evaluation_results/latest.json",
        "w",
        encoding="utf-8",
    ) as file:
        json.dump(
            {
                "model": settings.llm_model,
                "passed_checks": passed_checks,
                "total_checks": total_checks,
                "score": score,
                "cases": machine_results,
            },
            file,
            indent=2,
        )


if __name__ == "__main__":
    main()