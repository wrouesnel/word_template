from pathlib import Path

import dictdiffer
import logging
import os
import pprint
import pytest
import structlog

import sys

# Import the helpers
sys.path.append(os.path.join(os.path.dirname(__file__), "helpers"))

pp = pprint.PrettyPrinter(indent=2)


def pytest_assertrepr_compare(op, left, right):
    output = ["Compare Result:"]
    output.extend([pp.pformat(l) for l in list(dictdiffer.diff(left, right))])

    return output

@pytest.fixture
def root_dir() -> Path:
    start = Path(__file__).parent
    while not (start / "pytest.ini").exists():
        start = start.parent
    return start

@pytest.fixture
def log():
    """yield a structlog without initializing one through standard means"""
    # TODO: is this needed in this implementation?
    logging.basicConfig(level=logging.DEBUG, stream=sys.stderr)
    log = structlog.get_logger()

    structlog.configure(
        processors=[
            structlog.stdlib.filter_by_level,
            structlog.stdlib.add_logger_name,
            structlog.stdlib.add_log_level,
            structlog.stdlib.PositionalArgumentsFormatter(),
            structlog.processors.TimeStamper(fmt="%Y-%m-%d %H:%M:%S"),
            structlog.processors.StackInfoRenderer(),
            structlog.processors.format_exc_info,
            structlog.processors.UnicodeDecoder(),
            structlog.processors.KeyValueRenderer(),
        ],
        context_class=dict,
        logger_factory=structlog.stdlib.LoggerFactory(),
        wrapper_class=structlog.stdlib.BoundLogger,
        cache_logger_on_first_use=True,
    )

    yield log

