from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.messages import HumanMessage, SystemMessage

from agentic_qa.models import RequirementAnalysis


class LLMRequirementAnalyzer:
    def __init__(
        self,
        model: BaseChatModel,
    ) -> None:
        self._model = model.with_structured_output(
            RequirementAnalysis,
            method="json_schema",
            strict=True,
        )

    def analyze(
        self,
        requirement: str,
    ) -> RequirementAnalysis:
        messages = [
            SystemMessage(
                content=(
                    "You are a senior QA engineer analyzing software test requirements. "
                    "Extract only information supported by the requirement. "
                    "Do not design test steps. "
                    "Do not generate automation code. "
                    "Do not assume whether behavior is exposed through UI or API "
                    "unless the requirement makes this clear. "
                    "Classify interaction_surface using only evidence in the requirement. "
                    "Use 'ui' when the requirement explicitly refers to pages, screens, "
                    "forms, fields, buttons, dialogs, visible UI elements, or browser "
                    "navigation. "
                    "Use 'api' when it explicitly refers to HTTP methods, endpoints, "
                    "requests, responses, status codes, or API contracts. "
                    "Use 'system' for system-level or non-interactive behavior such as "
                    "concurrency, throughput, background processing, or resource behavior. "
                    "Otherwise use 'unknown'."
                    "Capture missing or unclear information in ambiguities. "
                    "Capture only material ambiguities: missing or unclear information "
                    "that could change the test design, expected behavior, required test "
                    "data, interaction surface, or interpretation of the requirement. "
                    "Do not enumerate every implementation detail that the requirement "
                    "does not mention. "
                    "Prefer a small number of high-value ambiguities."
                    "Do not invent missing behavior."
                    "Do not treat optional implementation details as ambiguities unless "
                    "they are necessary to verify the stated requirement."
                )
            ),
            HumanMessage(
                content=f"""
Analyze the following test requirement:

{requirement}
""".strip()
            ),
        ]

        result = self._model.invoke(messages)

        if not isinstance(result, RequirementAnalysis):
            raise TypeError("Requirement analyzer returned an unexpected result type.")

        return result
