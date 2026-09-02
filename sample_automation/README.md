# Sample Playwright Automation Framework

This is a small pytest + Playwright framework used by the
Agentic QA application as an example automation repository.

## Architecture

Tests
→ Fixtures
→ Page Objects
→ Playwright
→ Application

## Test conventions

- Use pytest.
- Use Playwright synchronous API consistently.
- Keep selectors inside Page Objects.
- Tests should describe user/business behavior.
- Prefer Playwright `expect`.
- Prefer user-facing locators:
  - `get_by_role`
  - `get_by_label`
  - `get_by_placeholder`
  - `get_by_test_id`
- Avoid CSS and XPath unless necessary.
- Do not use hard-coded sleeps.
- Reuse existing fixtures before creating new setup logic.
- Reuse existing Page Object methods before adding new ones.
- Keep tests small and focused.

## Running

```bash
uv run pytest sample_automation/tests -v