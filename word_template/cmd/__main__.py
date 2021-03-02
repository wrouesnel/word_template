"""Entrypoint script."""
from typing import List, Optional

import sys

from . import main


def entry(argv: Optional[List[str]] = None) -> None:
    """Entrypoint for the command script."""
    # Allow overriding command line params for debugging.
    if argv is not None:
        sys.argv = argv

    main(auto_envvar_prefix="WORD_TEMPLATE")


if __name__ == "__main__":
    entry()
