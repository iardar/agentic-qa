from pydantic import BaseModel, Field

from agentic_qa.models import InteractionSurface


class RequirementEvaluationCase(BaseModel):
    name: str
    requirement: str

    expected_surface: InteractionSurface

    required_condition_terms: list[str] = Field(
        default_factory=list
    )

    required_condition_alternatives: list[list[str]] = Field(
        default_factory=list
    )

    required_outcome_terms: list[str] = Field(
        default_factory=list
    )

    required_outcome_alternatives: list[list[str]] = Field(
        default_factory=list
    )

    require_ambiguities: bool | None = None
    
CASES = [
    # ------------------------------------------------------------------
    # Surface unknown / business-level requirements
    # ------------------------------------------------------------------

    RequirementEvaluationCase(
        name="simple_delete",
        requirement=(
            "User should be able to delete an existing component."
        ),
        expected_surface=InteractionSurface.UNKNOWN,
        required_condition_alternatives=[
            [
                "existing",
                "exists",
                "already exists",
                "available for deletion",
            ],
        ],
        required_outcome_alternatives=[
            [
                "delete",
                "deleted",
                "deletion",
                "remove",
                "removed",
            ],
        ],
    ),

    RequirementEvaluationCase(
        name="business_rule_referenced_component",
        requirement=(
            "Deleting a component that is referenced by another "
            "component should be prevented and an error should be displayed."
        ),
        expected_surface=InteractionSurface.UNKNOWN,
        required_condition_alternatives=[
            [
                "referenced",
                "has a reference",
                "dependency",
            ],
        ],
        required_outcome_terms=[
            "error",
        ],
        required_outcome_alternatives=[
            [
                "prevent",
                "blocked",
                "rejected",
                "not allowed",
                "cannot be deleted",
            ],
        ],
    ),

    RequirementEvaluationCase(
        name="authorization_delete",
        requirement=(
            "Only administrators should be able to delete components."
        ),
        expected_surface=InteractionSurface.UNKNOWN,
        required_outcome_alternatives=[
            [
                "administrators are able",
                "administrators can",
                "administrators are permitted",
                "administrator users can",
            ],
            [
                "non-administrator",
                "not permitted",
                "cannot delete",
                "not allowed",
                "forbidden",
            ],
        ],
        require_ambiguities=True,
    ),

    RequirementEvaluationCase(
        name="duplicate_component_name",
        requirement=(
            "A component cannot be created when another component "
            "with the same name already exists."
        ),
        expected_surface=InteractionSurface.UNKNOWN,
        required_condition_terms=[
            "same name",
        ],
        required_condition_alternatives=[
            [
                "exists",
                "already exists",
                "existing",
            ],
        ],
        required_outcome_alternatives=[
            [
                "cannot be created",
                "creation is prevented",
                "creation is rejected",
                "not created",
                "prevented",
            ],
        ],
    ),

    RequirementEvaluationCase(
        name="component_available_after_creation",
        requirement=(
            "After a component is created, it should be available "
            "for selection when creating a new project."
        ),
        expected_surface=InteractionSurface.UNKNOWN,
        required_condition_terms=[
            "project",
        ],
        required_condition_alternatives=[
            [
                "component is created",
                "component has been created",
                "component was created",
                "created component",
            ],
        ],
        required_outcome_alternatives=[
            [
                "available for selection",
                "can be selected",
                "selectable",
                "available to select",
            ],
        ],
    ),

    RequirementEvaluationCase(
        name="deleted_component_not_searchable",
        requirement=(
            "After a component is deleted, it should no longer "
            "appear in component search results."
        ),
        expected_surface=InteractionSurface.UNKNOWN,
        required_condition_alternatives=[
            [
                "deleted",
                "has been deleted",
                "removed",
            ],
        ],
        required_outcome_terms=[
            "search",
        ],
        required_outcome_alternatives=[
            [
                "no longer",
                "does not appear",
                "not appear",
                "excluded",
                "absent",
            ],
        ],
    ),

    RequirementEvaluationCase(
        name="search_interaction",
        requirement=(
            "Search results should update when the user "
            "enters a component name."
        ),
        expected_surface=InteractionSurface.UNKNOWN,
        required_outcome_alternatives=[
            [
                "update",
                "updated",
                "refresh",
                "refreshed",
            ],
        ],
        require_ambiguities=True,
    ),

    # ------------------------------------------------------------------
    # Explicit UI / E2E requirements
    # ------------------------------------------------------------------

    RequirementEvaluationCase(
        name="search_ui",
        requirement=(
            "On the Components page, search results should update "
            "when the user types a component name into the Search field."
        ),
        expected_surface=InteractionSurface.UI,
        required_condition_terms=[
            "Components page",
            "Search field",
        ],
        required_outcome_terms=[
            "search",
        ],
        required_outcome_alternatives=[
            [
                "update",
                "updated",
                "refresh",
                "refreshed",
                "filtered",
            ],
        ],
    ),

    RequirementEvaluationCase(
        name="create_component_ui",
        requirement=(
            "On the Components page, when the user creates a component "
            "with a valid name and clicks Save, the new component should "
            "appear in the component list."
        ),
        expected_surface=InteractionSurface.UI,
        required_condition_terms=[
            "Save",
        ],
        required_condition_alternatives=[
            [
                "valid name",
                "valid component name",
                "name is valid",
            ],
        ],
        required_outcome_terms=[
            "component",
            "list",
        ],
        required_outcome_alternatives=[
            [
                "appear",
                "shown",
                "displayed",
                "added",
            ],
        ],
    ),

    RequirementEvaluationCase(
        name="edit_component_ui",
        requirement=(
            "On the Edit Component page, changing the component description "
            "and clicking Save should update the description shown "
            "on the Component Details page."
        ),
        expected_surface=InteractionSurface.UI,
        required_condition_terms=[
            "description",
            "Save",
        ],
        required_outcome_terms=[
            "description",
        ],
        required_outcome_alternatives=[
            [
                "update",
                "updated",
                "reflect",
                "shown",
                "displayed",
            ],
        ],
    ),

    RequirementEvaluationCase(
        name="delete_confirmation_ui",
        requirement=(
            "When the user clicks Delete on the Components page, "
            "a confirmation dialog should appear before the component "
            "is permanently deleted."
        ),
        expected_surface=InteractionSurface.UI,
        required_condition_terms=[
            "Delete",
        ],
        required_outcome_terms=[
            "dialog",
        ],
        required_outcome_alternatives=[
            [
                "confirmation",
                "confirm deletion",
                "confirmation prompt",
            ],
            [
                "appear",
                "displayed",
                "shown",
                "opens",
            ],
        ],
    ),

    RequirementEvaluationCase(
        name="cancel_delete_ui",
        requirement=(
            "When the delete confirmation dialog is open and the user "
            "clicks Cancel, the dialog should close and the component "
            "should remain in the component list."
        ),
        expected_surface=InteractionSurface.UI,
        required_condition_terms=[
            "confirmation dialog",
            "Cancel",
        ],
        required_outcome_alternatives=[
            [
                "close",
                "closes",
                "closed",
                "dismissed",
            ],
            [
                "remain",
                "remains",
                "still present",
                "not deleted",
            ],
        ],
    ),

    RequirementEvaluationCase(
        name="login_success_ui",
        requirement=(
            "When a registered user enters valid credentials on the Login "
            "page and clicks Sign in, the Dashboard page should be displayed."
        ),
        expected_surface=InteractionSurface.UI,
        required_condition_terms=[
            "Login",
        ],
        required_condition_alternatives=[
            [
                "valid credentials",
                "correct credentials",
                "valid username and password",
            ],
        ],
        required_outcome_terms=[
            "Dashboard",
        ],
        required_outcome_alternatives=[
            [
                "displayed",
                "shown",
                "opened",
                "redirected",
                "navigated",
            ],
        ],
    ),

    RequirementEvaluationCase(
        name="login_invalid_password_ui",
        requirement=(
            "When a user enters a valid username and an invalid password "
            "on the Login page, an authentication error should be displayed "
            "and the user should remain on the Login page."
        ),
        expected_surface=InteractionSurface.UI,
        required_condition_alternatives=[
            [
                "invalid password",
                "incorrect password",
                "wrong password",
            ],
        ],
        required_outcome_terms=[
            "Login page",
        ],
        required_outcome_alternatives=[
            [
                "error",
                "authentication failure",
                "login failed",
                "rejected",
            ],
            [
                "remain",
                "stays",
                "does not navigate",
                "not redirected",
            ],
        ],
    ),

    RequirementEvaluationCase(
        name="protected_page_ui",
        requirement=(
            "When an unauthenticated user opens the Components page, "
            "the browser should redirect the user to the Login page."
        ),
        expected_surface=InteractionSurface.UI,
        required_condition_terms=[
            "Components page",
        ],
        required_condition_alternatives=[
            [
                "unauthenticated",
                "not authenticated",
                "not logged in",
                "signed out",
            ],
        ],
        required_outcome_terms=[
            "Login page",
        ],
        required_outcome_alternatives=[
            [
                "redirect",
                "redirected",
                "sent",
                "navigated",
            ],
        ],
    ),

    RequirementEvaluationCase(
        name="session_timeout_ui",
        requirement=(
            "After 30 minutes of inactivity, the user's session should "
            "expire and the user should be redirected to the Login page."
        ),
        expected_surface=InteractionSurface.UI,
        required_condition_terms=[
            "30 minutes",
        ],
        required_condition_alternatives=[
            [
                "inactivity",
                "inactive",
                "no activity",
            ],
        ],
        required_outcome_terms=[
            "Login page",
        ],
        required_outcome_alternatives=[
            [
                "expire",
                "expired",
                "expires",
                "timeout",
                "times out",
                "invalidated",
            ],
            [
                "redirect",
                "redirected",
                "sent",
                "navigated",
            ],
        ],
    ),

    # ------------------------------------------------------------------
    # Explicit API / integration requirements
    # ------------------------------------------------------------------

    RequirementEvaluationCase(
        name="api_create_component",
        requirement=(
            "POST /components with a valid component name should create "
            "the component and return HTTP 201."
        ),
        expected_surface=InteractionSurface.API,
        required_condition_alternatives=[
            [
                "valid component name",
                "valid name",
                "component name is valid",
            ],
        ],
        required_outcome_terms=[
            "201",
        ],
        required_outcome_alternatives=[
            [
                "create",
                "created",
                "creation succeeds",
            ],
        ],
    ),

    RequirementEvaluationCase(
        name="api_missing_component_name",
        requirement=(
            "POST /components should return HTTP 400 "
            "when the component name is missing."
        ),
        expected_surface=InteractionSurface.API,
        required_condition_terms=[
            "component name",
        ],
        required_condition_alternatives=[
            [
                "missing",
                "omitted",
                "absent",
                "not provided",
            ],
        ],
        required_outcome_terms=[
            "400",
        ],
    ),

    RequirementEvaluationCase(
        name="api_duplicate_component",
        requirement=(
            "POST /components should return HTTP 409 when a component "
            "with the same name already exists."
        ),
        expected_surface=InteractionSurface.API,
        required_condition_terms=[
            "same name",
        ],
        required_condition_alternatives=[
            [
                "exists",
                "already exists",
                "existing",
            ],
        ],
        required_outcome_terms=[
            "409",
        ],
    ),

    RequirementEvaluationCase(
        name="api_get_component",
        requirement=(
            "GET /components/{id} should return HTTP 200 and the component "
            "details when the requested component exists."
        ),
        expected_surface=InteractionSurface.API,
        required_condition_alternatives=[
            [
                "exists",
                "existing",
                "already exists",
                "is present",
            ],
        ],
        required_outcome_terms=[
            "200",
        ],
        required_outcome_alternatives=[
            [
                "details",
                "component data",
                "component information",
                "component representation",
            ],
        ],
    ),

    RequirementEvaluationCase(
        name="api_component_not_found",
        requirement=(
            "GET /components/{id} should return HTTP 404 "
            "when the requested component does not exist."
        ),
        expected_surface=InteractionSurface.API,
        required_condition_alternatives=[
            [
                "does not exist",
                "doesn't exist",
                "not exist",
                "non-existent",
                "not found",
                "absent",
            ],
        ],
        required_outcome_terms=[
            "404",
        ],
    ),

    RequirementEvaluationCase(
        name="api_update_component",
        requirement=(
            "PUT /components/{id} with a valid description should update "
            "the existing component and return HTTP 200."
        ),
        expected_surface=InteractionSurface.API,
        required_condition_alternatives=[
            [
                "existing",
                "exists",
                "already exists",
            ],
            [
                "valid description",
                "description is valid",
                "valid component description",
            ],
        ],
        required_outcome_terms=[
            "200",
        ],
        required_outcome_alternatives=[
            [
                "update",
                "updated",
                "modified",
                "changed",
            ],
        ],
    ),

    RequirementEvaluationCase(
        name="api_delete_referenced_component",
        requirement=(
            "DELETE /components/{id} should return HTTP 409 and leave "
            "the component unchanged when it is referenced by another component."
        ),
        expected_surface=InteractionSurface.API,
        required_condition_alternatives=[
            [
                "referenced",
                "has a reference",
                "dependency",
            ],
        ],
        required_outcome_terms=[
            "409",
        ],
        required_outcome_alternatives=[
            [
                "unchanged",
                "not modified",
                "remains unchanged",
                "preserved",
            ],
        ],
    ),

    RequirementEvaluationCase(
        name="api_unauthorized_delete",
        requirement=(
            "DELETE /components/{id} should return HTTP 403 when "
            "the authenticated user does not have permission to delete components."
        ),
        expected_surface=InteractionSurface.API,
        required_condition_alternatives=[
            [
                "does not have permission",
                "without permission",
                "lacks permission",
                "not authorized",
                "unauthorized",
            ],
        ],
        required_outcome_terms=[
            "403",
        ],
    ),

    # ------------------------------------------------------------------
    # Deliberately incomplete requirements
    # ------------------------------------------------------------------

    RequirementEvaluationCase(
        name="ambiguous_delete",
        requirement="Verify component deletion.",
        expected_surface=InteractionSurface.UNKNOWN,
        require_ambiguities=True,
    ),

    RequirementEvaluationCase(
        name="ambiguous_login",
        requirement="Verify login.",
        expected_surface=InteractionSurface.UNKNOWN,
        require_ambiguities=True,
    ),

    RequirementEvaluationCase(
        name="ambiguous_component_validation",
        requirement=(
            "Component data should be validated."
        ),
        expected_surface=InteractionSurface.UNKNOWN,
        require_ambiguities=True,
    ),
]