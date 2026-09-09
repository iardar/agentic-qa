from agentic_qa.evals.retrieval.models import RetrievalEvaluationCase
from agentic_qa.models import InteractionSurface, RequirementAnalysis

REAL_WORLD_CASES = [
    RetrievalEvaluationCase(
        name="realworld_login",
        analysis=RequirementAnalysis(
            feature="User authentication",
            operation="Sign in with registered credentials",
            objective=(
                "Verify that a registered user can sign in "
                "using a valid email and password and that "
                "their username is displayed in the "
                "application navigation after successful "
                "sign-in."
            ),
            actors=[
                "Registered user",
            ],
            conditions=[
                "The user is on the Sign in page.",
                "The user has a valid registered email and password.",
            ],
            expected_outcomes=[
                "The user can successfully sign in using the valid email and password.",
                ("The signed-in user's username is visible in the application navigation."),
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
            operation=("Sign in with a valid registered email and an invalid password"),
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
                ("The user enters a valid email associated with a registered user."),
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
    RetrievalEvaluationCase(
        name="realworld_registration",
        analysis=RequirementAnalysis(
            feature="User registration",
            operation="Register a new user",
            objective=(
                "Verify that a new user can register using "
                "a unique username, valid email, and password "
                "and that their username is displayed in the "
                "application navigation."
            ),
            actors=[
                "New user",
            ],
            conditions=[
                "The user is on the Sign up page.",
                "A unique username is provided.",
                "A valid email is provided.",
                "A password is provided.",
            ],
            expected_outcomes=[
                "The user is registered successfully.",
                ("The registered user's username is visible in the application navigation."),
            ],
            ambiguities=[],
            interaction_surface=InteractionSurface.UI,
        ),
        required_paths=[
            "tests/auth/test_registration.py",
            "pages/register_page.py",
            "fixtures/users.py",
            "components/navigation.py",
        ],
    ),
    RetrievalEvaluationCase(
        name="realworld_missing_username_registration",
        analysis=RequirementAnalysis(
            feature="User registration",
            operation=(
                "Attempt to sign up with a valid email "
                "and password while leaving the username empty"
            ),
            objective=(
                "Verify that registration cannot be submitted "
                "when the username is empty, even if the email "
                "and password are valid."
            ),
            actors=[
                "User",
            ],
            conditions=[
                "The user is on the Sign up page.",
                "A valid email is provided.",
                "A valid password is provided.",
                "The username is left empty.",
            ],
            expected_outcomes=[
                "The Sign up button remains disabled.",
                "The registration form is not submitted.",
            ],
            ambiguities=[],
            interaction_surface=InteractionSurface.UI,
        ),
        required_paths=[
            "tests/auth/test_invalid_registration.py",
            "pages/register_page.py",
            "fixtures/users.py",
        ],
    ),
]
