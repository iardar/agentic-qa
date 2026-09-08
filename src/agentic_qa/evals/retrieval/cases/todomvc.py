from agentic_qa.evals.retrieval.models import RetrievalEvaluationCase
from agentic_qa.models import InteractionSurface, RequirementAnalysis

TODOMVC_CASES = [
    RetrievalEvaluationCase(
        name="complete_existing_todo",
        analysis=RequirementAnalysis(
            feature="Todo management",
            operation="Complete an existing todo",
            objective=(
                "Verify that a user can complete "
                "a todo that already exists."
            ),
            actors=[
                "User",
            ],
            conditions=[
                "A todo already exists.",
            ],
            expected_outcomes=[
                "The user is able to complete "
                "the existing todo.",
            ],
            ambiguities=[],
            interaction_surface=(
                InteractionSurface.UNKNOWN
            ),
        ),
        required_paths=[
            "tests/test_todo_completion.py",
            "pages/todo_page.py",
            "tests/conftest.py",
        ],
    ),
    RetrievalEvaluationCase(
        name="create_todo",
        analysis=RequirementAnalysis(
            feature="Todo management",
            operation="Create a new todo",
            objective=(
                "Verify that a user can create "
                "a new todo."
            ),
            actors=[
                "User",
            ],
            conditions=[],
            expected_outcomes=[
                "A new todo is created.",
            ],
            ambiguities=[],
            interaction_surface=(
                InteractionSurface.UNKNOWN
            ),
        ),
        required_paths=[
            "tests/test_todo_creation.py",
            "pages/todo_page.py",
            "tests/conftest.py",
        ],
    ),
    RetrievalEvaluationCase(
        name="mark_task_as_done",
        analysis=RequirementAnalysis(
            feature="Task management",
            operation="Mark an existing task as done",
            objective=(
                "Verify that a user can mark "
                "an existing task as done."
            ),
            actors=[
                "User",
            ],
            conditions=[
                "An existing task is available.",
            ],
            expected_outcomes=[
                "The task is marked as done.",
            ],
            ambiguities=[],
            interaction_surface=(
                InteractionSurface.UNKNOWN
            ),
        ),
        required_paths=[
            "tests/test_todo_completion.py",
            "pages/todo_page.py",
            "tests/conftest.py",
        ],
    ),
]