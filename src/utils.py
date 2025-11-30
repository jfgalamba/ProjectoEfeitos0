"""
Generic utilities for this project.

--------------------------------------------------------------------------------

(C) João Galamba, 2025
Código sob licença MIT. Consultar: https://mit-license.org/
"""

from typing import (
    Any,
    Iterator,
    Protocol,
    Reversible,
    Sized,
    runtime_checkable
)


__all__ = (
    'renumerate',
    'SizedReversible',
    'IndexedSizedReversible',
)

@runtime_checkable
class SizedReversible(Sized, Reversible, Protocol):
    """Sized + reversible collections."""

@runtime_checkable
class IndexedSizedReversible(Sized, Reversible, Protocol):
    """Indexed + SizedReversible"""
    def __getitem__(self, key: int) -> Any: ...

# OU:
#   @runtime_checkable
#   class SizedReversible(Protocol):
#       def __len__(self) -> int: ...
#       def __iter__(self) -> Iterator[object]: ...
#       def __reversed__(self) -> Iterator[object]: ...
# #:

def renumerate(
        collection: SizedReversible,
        start_at: int | None = None
) -> Iterator[tuple[int, Any]]:
    """
    Enumerate in reverse order starting from len(collection)-1 by
    default. 

    Note that renumerate, unlike enumerate, needs a reversible 
    collection (or iterable) with a length. There has to be a way to
    reach the end of the collection, either by ensuring that it has a
    length and that is indexable, or by ensuring that it is reversible.
    But even in this last case - being reversible - we still need a
    length so that we return a counter for each element in the
    collection.

    Args:
        collection: Sized reversible collection or iterable (list, 
            tuple, str, deque, etc.). Collections/iterables that 
            renumerate won't accept: set, any generator, generator
            expressions, etc.
        start_at: Starting index (None = len(collection)-1)

    Returns:
        Iterator of (index, item) tuples in reverse order

    Examples:
        >>> list(renumerate([10, 20, 30, 40]))
        [(3, 40), (2, 30), (1, 20), (0, 10)]
        >>> list(renumerate([10, "hello", 3.14], 100))
        [(2, 3.14), (1, 'hello'), (0, 10)]
    """
    counter = start_at if start_at is not None else len(collection) - 1 
    for item in reversed(collection):
        yield counter, item
        counter -= 1
#:

# ALTERNATIVE IMPLEMENTATION
# def renumerate(
#         collection: SizedReversible,
#         start_at: int | None = None
# ) -> Iterator[tuple[int, Any]]:
#     end_at = (start_at - len(collection)) if start_at is not None else -1
#     start_at = start_at if start_at is not None else len(collection) - 1
#     return zip(range(start_at, end_at, -1), reversed(collection))


