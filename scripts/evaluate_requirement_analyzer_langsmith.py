from typing import Any
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langsmith import Client

from agentic_qa.config import settings
from agentic_qa.evals.requirements.cases import (
    RequirementEvaluationCase,
)
from agentic_qa.evals.requirements.evaluator import (
    evaluate_analysis,
)
from agentic_qa.models import (
    InteractionSurface,
    RequirementAnalysis,
)
from agentic_qa.requirements.llm_analyzer import (
    LLMRequirementAnalyzer,
)

load_dotenv()
DATASET_NAME = "requirement-analyzer-v1"


def create_analyzer() -> LLMRequirementAnalyzer:
    if settings.openai_api_key is None:
        raise RuntimeError(
            "OPENAI_API_KEY is not configured."
        )

    model = ChatOpenAI(
        model=settings.llm_model,
        api_key=settings.openai_api_key,
    )

    return LLMRequirementAnalyzer(
        model=model
    )


analyzer = create_analyzer()


def target(
    inputs: dict[str, Any],
) -> dict[str, Any]:
    analysis = analyzer.analyze(
        inputs["requirement"]
    )

    return {
        "analysis": analysis.model_dump(
            mode="json"
        ),
    }

def build_case(
    inputs: dict[str, Any],
    reference_outputs: dict[str, Any],
) -> RequirementEvaluationCase:
    return RequirementEvaluationCase(
        name="langsmith_case",
        requirement=inputs["requirement"],
        expected_surface=InteractionSurface(
            reference_outputs[
                "expected_surface"
            ]
        ),
        required_condition_terms=(
            reference_outputs.get(
                "required_condition_terms",
                [],
            )
        ),
        required_condition_alternatives=(
            reference_outputs.get(
                "required_condition_alternatives",
                [],
            )
        ),
        required_outcome_terms=(
            reference_outputs.get(
                "required_outcome_terms",
                [],
            )
        ),
        required_outcome_alternatives=(
            reference_outputs.get(
                "required_outcome_alternatives",
                [],
            )
        ),
        require_ambiguities=(
            reference_outputs.get(
                "require_ambiguities"
            )
        ),
    )


def requirement_analysis_evaluator(
    inputs: dict[str, Any],
    outputs: dict[str, Any],
    reference_outputs: dict[str, Any],
) -> list[dict[str, Any]]:
    analysis = RequirementAnalysis.model_validate(
        outputs["analysis"]
    )

    case = build_case(
        inputs,
        reference_outputs,
    )

    checks = evaluate_analysis(
        analysis,
        case,
    )

    return [
        {
            "key": check.name,
            "score": check.passed,
            "comment": check.message,
        }
        for check in checks
    ]


def case_pass_evaluator(
    inputs: dict[str, Any],
    outputs: dict[str, Any],
    reference_outputs: dict[str, Any],
) -> dict[str, Any]:
    analysis = RequirementAnalysis.model_validate(
        outputs["analysis"]
    )

    case = build_case(
        inputs,
        reference_outputs,
    )

    checks = evaluate_analysis(
        analysis,
        case,
    )

    passed = all(
        check.passed
        for check in checks
    )

    failed_checks = [
        check.name
        for check in checks
        if not check.passed
    ]

    return {
        "key": "case_pass",
        "score": passed,
        "comment": (
            "all checks passed"
            if passed
            else (
                "failed checks: "
                + ", ".join(failed_checks)
            )
        ),
    }


def main() -> None:
    client = Client()

    results = client.evaluate(
        target,
        data=DATASET_NAME,
        evaluators=[
            requirement_analysis_evaluator,
            case_pass_evaluator,
        ],
        experiment_prefix=(
            "requirement-analyzer"
        ),
        max_concurrency=2,
        metadata={
            "model": settings.llm_model,
            "component": (
                "requirement_analyzer"
            ),
            "analyzer_version": "v1",
        },
    )

    print(results)


if __name__ == "__main__":
    main()