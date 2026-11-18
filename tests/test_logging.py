"""Tests for the logging setup done when the library is imported.

They run in a child interpreter, where logging starts from a clean slate: in
the test process pytest has already put its own handlers on the root logger.
"""

import json
import logging
import os
import re
import subprocess
import sys
from pathlib import Path

import outfancy

# Folder that holds the package under test, so the child imports the same one.
PACKAGE_PARENT = str(Path(outfancy.__file__).resolve().parent.parent)


def run_python(code):
    """Run ``code`` in a fresh interpreter and return the finished process."""
    env = {**os.environ, "PYTHONPATH": PACKAGE_PARENT}
    result = subprocess.run(
        [sys.executable, "-c", code],
        env=env, capture_output=True, encoding="utf-8",
    )
    assert result.returncode == 0, result.stderr
    return result


class TestRootLogger:
    def test_importing_the_library_leaves_the_root_logger_alone(self):
        # The application that imports outfancy decides where its logs go.
        code = (
            "import json, logging, outfancy.chart, outfancy.table\n"
            "root = logging.getLogger()\n"
            "handlers = [type(handler).__name__ for handler in root.handlers]\n"
            "print(json.dumps({'handlers': handlers, 'level': root.level}))\n"
        )
        state = json.loads(run_python(code).stdout)
        assert state == {"handlers": [], "level": logging.WARNING}


class TestLibraryLogger:
    # The defaults that LOGGING.md documents.

    def test_warnings_go_to_stderr_by_default(self):
        code = (
            "import logging, outfancy.table\n"
            "logging.getLogger('outfancy').warning('label_list was rebuilt')\n"
        )
        result = run_python(code)
        assert result.stdout == ""
        assert re.search(
            r"^\d{4}-\d\d-\d\d \d\d:\d\d:\d\d - outfancy - WARNING - "
            r"label_list was rebuilt$",
            result.stderr, re.MULTILINE,
        )

    def test_info_is_hidden_by_default(self):
        code = (
            "import logging, outfancy.table\n"
            "logging.getLogger('outfancy').info('rendered 3 rows')\n"
        )
        assert "rendered 3 rows" not in run_python(code).stderr
