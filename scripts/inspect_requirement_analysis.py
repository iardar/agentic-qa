from langchain_openai import ChatOpenAI

from agentic_qa.config import settings
from agentic_qa.requirements.llm_analyzer import (
    LLMRequirementAnalyzer,
)


REQUIREMENTS = [
    (
        "simple_delete",
        "User should be able to delete an existing component.",
    ),
    (
        "business_rule",
        (
            "Deleting a component that is referenced by another "
            "component should be prevented and an error should be displayed."
        ),
    ),
    (
        "api_validation",
        (
            "POST /components should return HTTP 400 "
            "when the component name is missing."
        ),
    ),
    (
        "authorization",
        "Only administrators should be able to delete components.",
    ),
    (
        "search_interaction",
        (
            "Search results should update when the user "
            "enters a component name."
        ),
    ),
    (
        "search_ui",
        (
            "On the Components page, search results should update"
            "when the user types a component name into the Search field."        
        ),
    ),
    (
        "performance",
        (
            "The system should support 100 concurrent users "
            "searching for components without significant degradation."
        ),
    ),
    (
        "ambiguous",
        "Verify component deletion.",
    ),
    (
        "session",
        (
            "After 30 minutes of inactivity, the user's session "
            "should expire and the user should be redirected "
            "to the login page."
        ),
    ),
]


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
        api_key=settings.openai_api_key.get_secret_value(),
    )

    analyzer = LLMRequirementAnalyzer(
        model=model,
    )

    for name, requirement in REQUIREMENTS:
        print("=" * 80)
        print(f"CASE: {name}")
        print()
        print("REQUIREMENT:")
        print(requirement)
        print()

        result = analyzer.analyze(requirement)

        print("ANALYSIS:")
        print(
            result.model_dump_json(
                indent=2,
            )
        )

        print()


if __name__ == "__main__":
    main()