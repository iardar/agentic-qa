from pydantic import BaseModel, Field
from dotenv import load_dotenv

from agentic_qa.models import (
    InteractionSurface,
    RequirementAnalysis,
)

load_dotenv()

class RetrievalEvaluationCase(BaseModel):
    name: str

    analysis: RequirementAnalysis

    required_paths: list[str] = Field(
        default_factory=list
    )


CASES = [
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
    RetrievalEvaluationCase(
        name="realworld_login",
        analysis=RequirementAnalysis(
            feature="User authentication",
            operation="Sign in with registered user credentials",
            objective=(
                "Verify that a registered user can sign in "
                "using a valid email and password and that "
                "their username is displayed in the "
                "application navigation."
            ),
            actors=[
                "Registered user",
            ],
            conditions=[
                "The user is registered.",
                "A valid email and password are used.",
                "The operation occurs on the Sign in page.",
            ],
            expected_outcomes=[
                "The registered user can sign in successfully.",
                (
                    "The user's username is visible in the "
                    "application navigation after successful "
                    "sign-in."
                ),
            ],
            ambiguities=[],
            interaction_surface=InteractionSurface.UI,
        ),
        required_paths=[
            "tests/auth/test_login.py",
            "pages/login_page.py",
            "fixtures/users.py",
            "components/navigation.py",
        ],
    ),
]