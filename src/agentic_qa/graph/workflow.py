from typing import Any

from langgraph.graph import END, START, StateGraph
from langgraph.graph.state import CompiledStateGraph

from agentic_qa.graph.nodes import (
    analyze_result,
    create_analyze_requirement_node,
    create_retrieve_context_node,
    design_test,
    explore_ui,
    generate_test,
    run_test,
)
from agentic_qa.graph.state import QAState
from agentic_qa.requirements.analyzer import RequirementAnalyzer
from agentic_qa.retrieval.provider import RepositoryContextProvider


def build_workflow(
    requirement_analyzer: RequirementAnalyzer,
    repository_context_provider: RepositoryContextProvider,
) -> CompiledStateGraph[
    QAState,
    None,
    QAState,
    QAState,
]:
    graph = StateGraph(QAState)

    graph.add_node(
        "analyze_requirement",
        create_analyze_requirement_node(requirement_analyzer),
    )
    graph.add_node(
        "retrieve_context",
        create_retrieve_context_node(repository_context_provider),
    )
    graph.add_node("explore_ui", explore_ui)
    graph.add_node("design_test", design_test)
    graph.add_node("generate_test", generate_test)
    graph.add_node("run_test", run_test)
    graph.add_node("analyze_result", analyze_result)

    graph.add_edge(START, "analyze_requirement")

    graph.add_edge(
        "analyze_requirement",
        "retrieve_context",
    )

    graph.add_edge(
        "retrieve_context",
        "explore_ui",
    )

    graph.add_edge(
        "explore_ui",
        "design_test",
    )

    graph.add_edge(
        "design_test",
        "generate_test",
    )

    graph.add_edge(
        "generate_test",
        "run_test",
    )

    graph.add_edge(
        "run_test",
        "analyze_result",
    )

    graph.add_edge(
        "analyze_result",
        END,
    )

    return graph.compile()
