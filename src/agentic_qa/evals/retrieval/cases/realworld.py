
from dotenv import load_dotenv

from agentic_qa.evals.retrieval.models import RetrievalEvaluationCase
from agentic_qa.models import InteractionSurface, RequirementAnalysis

load_dotenv()


REALWORLD_CASES = [
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

    RetrievalEvaluationCase(
            name="realworld_invalid_password_login",
            analysis=RequirementAnalysis(
                feature="User authentication",
                operation=(
                    "Sign in with a valid registered email "
                    "and an invalid password"
                ),
                objective=(
                    "Verify that an unsuccessful sign-in attempt "
                    "displays an authentication error and keeps "
                    "the user on the Sign in page."
                ),
                actors=[
                    "Registered user",
                ],
                conditions=[
                    "The user is on the Sign in page.",
                    (
                        "The user enters a valid email associated "
                        "with a registered user."
                    ),
                    "The user enters an invalid password.",
                    "The user clicks Sign in.",
                ],
                expected_outcomes=[
                    "An authentication error is displayed.",
                    "The user remains on the Sign in page.",
                ],
                ambiguities=[],
                interaction_surface=InteractionSurface.UI,
            ),
            required_paths=[
                "tests/auth/test_invalid_login.py",
                "pages/login_page.py",
                "fixtures/users.py",
            ],
        ),
    ]
