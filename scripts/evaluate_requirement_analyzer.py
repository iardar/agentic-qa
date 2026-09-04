import json
from pathlib import Path

from langchain_openai import ChatOpenAI

from agentic_qa.config import settings
from agentic_qa.evals.requirements.cases import CASES
from agentic_qa.evals.requirements.evaluator import evaluate_analysis
from agentic_qa.requirements.llm_analyzer import LLMRequirementAnalyzer


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
        api_key=settings.openai_api_key,
    )

    analyzer = LLMRequirementAnalyzer(
        model=model
    )

    total_checks = 0
    passed_checks = 0

    machine_results: list[dict[str, object]] = []

    print(f"MODEL: {settings.llm_model}")
    print()

    for case in CASES:
        print("=" * 80)
        print(f"CASE: {case.name}")
        print()

        analysis = analyzer.analyze(
            case.requirement
        )

        checks = evaluate_analysis(
            analysis=analysis,
            case=case,
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
                "analysis": analysis.model_dump(
                    mode="json"
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
        else 0.0
    )

    print("=" * 80)
    print("SUMMARY")
    print()
    print(
        f"Passed: {passed_checks}/{total_checks}"
    )
    print(
        f"Check score: {score:.1%}"
    )

    output_dir = Path(
        "evaluation_results"
    )

    output_dir.mkdir(
        parents=True,
        exist_ok=True,
    )

    output_file = (
        output_dir / "latest.json"
    )

    with output_file.open(
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