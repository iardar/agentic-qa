from typing import Protocol


class RepositoryContextProvider(Protocol):
    def search(
        self,
        query: str,
    ) -> list[str]:
        """Return repository context relevant to the query."""
        ...
