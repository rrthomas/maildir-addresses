"""maildir-addresses tests.

© Reuben Thomas <rrt@sc3d.org> 2026

Released under the GPL version 3, or (at your option) any later version.
"""

from pathlib import Path

import pytest
from pytest import CaptureFixture, LogCaptureFixture
from testutils import failing_cli_test

from maildir_addresses import main


tests_dir = Path(__file__).parent.resolve() / "test-files"


# CLI tests
def test_help_option_should_produce_output(capsys: CaptureFixture[str]) -> None:
    with pytest.raises(SystemExit) as e:
        main(["--help"])
    assert e.type is SystemExit
    assert e.value.code == 0
    assert (
        capsys.readouterr().out.find(
            "Scan a maildir tree for email addresses in From/To/Cc headers"
        )
        != -1
    )


def test_invalid_command_line_argument_causes_an_error(
    capsys: CaptureFixture[str],
    caplog: LogCaptureFixture,
) -> None:
    failing_cli_test(capsys, caplog, ["--foo", "foo"], "unrecognized arguments: --foo")
