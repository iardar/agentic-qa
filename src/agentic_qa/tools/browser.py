from typing import Protocol


class BrowserExplorer(Protocol):
    async def explore(
        self,
        objective: str,
    ) -> list[str]:
        """Explore the live application and return observed facts."""
        ...
