import ast
from collections.abc import Iterator
from pathlib import Path

from agentic_qa.retrieval.symbols.models import (
    RepositorySymbol,
    RepositorySymbolIndex,
    SymbolType,
)


class PythonAstSymbolIndexer:
    SUPPORTED_SUFFIXES = {
        ".py",
    }

    IGNORED_DIRECTORIES = {
        ".git",
        ".venv",
        "__pycache__",
        ".pytest_cache",
        ".mypy_cache",
        ".ruff_cache",
    }

    def __init__(
        self,
        repository_path: Path,
    ) -> None:
        self._repository_path = repository_path

    def build_index(self) -> RepositorySymbolIndex:
        self._validate_repository()

        symbols: list[RepositorySymbol] = []

        for path in self._iter_source_files():
            symbols.extend(self._index_file(path))

        return RepositorySymbolIndex(symbols=symbols)

    def _validate_repository(self) -> None:
        if not self._repository_path.exists():
            raise FileNotFoundError(f"Repository does not exist: {self._repository_path}")

        if not self._repository_path.is_dir():
            raise NotADirectoryError(f"Repository path is not a directory: {self._repository_path}")

    def _iter_source_files(self) -> Iterator[Path]:
        for path in self._repository_path.rglob("*"):
            if not path.is_file():
                continue

            if path.suffix not in self.SUPPORTED_SUFFIXES:
                continue

            if self._should_ignore(path):
                continue

            yield path

    def _should_ignore(
        self,
        path: Path,
    ) -> bool:
        return any(part in self.IGNORED_DIRECTORIES for part in path.parts)

    def _index_file(
        self,
        path: Path,
    ) -> list[RepositorySymbol]:
        content = path.read_text(encoding="utf-8")

        tree = ast.parse(
            content,
            filename=str(path),
        )

        relative_path = path.relative_to(self._repository_path)

        symbols: list[RepositorySymbol] = []

        for node in tree.body:
            if isinstance(node, ast.ClassDef):
                symbols.extend(
                    self._index_class(
                        node=node,
                        path=relative_path,
                        content=content,
                    )
                )

            elif isinstance(
                node,
                (ast.FunctionDef, ast.AsyncFunctionDef),
            ):
                symbols.append(
                    self._create_function_symbol(
                        node=node,
                        path=relative_path,
                        content=content,
                    )
                )

        return symbols

    def _index_class(
        self,
        node: ast.ClassDef,
        path: Path,
        content: str,
    ) -> list[RepositorySymbol]:
        symbols = [
            RepositorySymbol(
                name=node.name,
                qualified_name=node.name,
                symbol_type=SymbolType.CLASS,
                path=str(path),
                start_line=node.lineno,
                end_line=self._end_line(node),
                source=self._source_segment(
                    node=node,
                    content=content,
                ),
                decorators=self._decorators(node.decorator_list),
                bases=[ast.unparse(base) for base in node.bases],
            )
        ]

        for child in node.body:
            if not isinstance(
                child,
                (
                    ast.FunctionDef,
                    ast.AsyncFunctionDef,
                ),
            ):
                continue

            symbols.append(
                RepositorySymbol(
                    name=child.name,
                    qualified_name=(f"{node.name}.{child.name}"),
                    symbol_type=SymbolType.METHOD,
                    path=str(path),
                    parent=node.name,
                    start_line=child.lineno,
                    end_line=self._end_line(child),
                    source=self._source_segment(
                        node=child,
                        content=content,
                    ),
                    parameters=self._parameters(child.args),
                    decorators=self._decorators(child.decorator_list),
                )
            )

        return symbols

    def _create_function_symbol(
        self,
        node: ast.FunctionDef | ast.AsyncFunctionDef,
        path: Path,
        content: str,
    ) -> RepositorySymbol:
        decorators = self._decorators(node.decorator_list)

        return RepositorySymbol(
            name=node.name,
            qualified_name=node.name,
            symbol_type=self._function_type(
                name=node.name,
                decorators=decorators,
            ),
            path=str(path),
            start_line=node.lineno,
            end_line=self._end_line(node),
            source=self._source_segment(
                node=node,
                content=content,
            ),
            parameters=self._parameters(node.args),
            decorators=decorators,
        )

    def _function_type(
        self,
        name: str,
        decorators: list[str],
    ) -> SymbolType:
        if name.startswith("test_"):
            return SymbolType.TEST

        if any(
            decorator == "pytest.fixture"
            or decorator.startswith("pytest.fixture(")
            or decorator == "fixture"
            or decorator.startswith("fixture(")
            for decorator in decorators
        ):
            return SymbolType.FIXTURE

        return SymbolType.FUNCTION

    def _parameters(
        self,
        arguments: ast.arguments,
    ) -> list[str]:
        parameters = [
            argument.arg
            for argument in (
                *arguments.posonlyargs,
                *arguments.args,
            )
        ]

        if arguments.vararg is not None:
            parameters.append(arguments.vararg.arg)

        parameters.extend(argument.arg for argument in arguments.kwonlyargs)

        if arguments.kwarg is not None:
            parameters.append(arguments.kwarg.arg)

        return parameters

    def _decorators(
        self,
        decorators: list[ast.expr],
    ) -> list[str]:
        return [ast.unparse(decorator) for decorator in decorators]

    def _source_segment(
        self,
        node: ast.AST,
        content: str,
    ) -> str:
        source = ast.get_source_segment(
            content,
            node,
        )

        return source or ""

    def _end_line(
        self,
        node: ast.ClassDef | ast.FunctionDef | ast.AsyncFunctionDef,
    ) -> int:
        if node.end_lineno is not None:
            return node.end_lineno

        return node.lineno
