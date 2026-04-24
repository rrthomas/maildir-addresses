"""maildir-addresses: Main module.

© Reuben Thomas <rrt@sc3d.org> 2026.

Released under the GPL version 3, or (at your option) any later version.
"""

import argparse
import csv
import importlib.metadata
import logging
import mailbox
import os
import sys
import warnings
from email.utils import getaddresses
from pathlib import Path

from .subcommand import commands
from .warnings_util import die, simple_warning, warn


VERSION = importlib.metadata.version("maildir_addresses")


csv.register_dialect("mailcsv", skipinitialspace=True)


def parse_maildir(maildir_path: os.PathLike) -> None:
    emails = {}

    # Open Maildir
    mbox = mailbox.Maildir(maildir_path)
    for key in mbox.iterkeys():
        message = mbox[key]

        # Check headers: From, To, Cc
        for header in ("From", "To", "Cc"):
            addrs = getaddresses(message.get_all(header, []))
            for name, addr in addrs:
                emails[addr.lower()] = name

    # Output results
    for mail in sorted(emails):
        print(f'"{emails[mail]}" <{mail}>')


def walk_die(err):
    raise err


def parse_maildirs(maildir_root: Path) -> None:
    for dirpath, dirs, _ in maildir_root.walk(on_error=walk_die):
        # TODO: Make this list configurable
        if dirpath.name.lower() in (".junk", ".spam"):
            continue
        if "cur" in dirs and "new" in dirs and "tmp" in dirs:
            warn(f"processing {dirpath}")
            parse_maildir(dirpath)


def main(argv: list[str] = sys.argv[1:]) -> None:
    # Command-line arguments
    parser = argparse.ArgumentParser(
        description="Scan a maildir tree for email addresses in From/To/Cc headers",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "-V",
        "--version",
        action="version",
        version=f"""%(prog)s {VERSION}
© 2026 Reuben Thomas <rrt@sc3d.org>
https://github.com/rrthomas/maildir-addresses
Distributed under the GNU General Public License version 3, or (at
your option) any later version. There is no warranty.""",
    )
    parser.add_argument(
        "mail_root",
        metavar="MAIL-DIRECTORY",
        help="maildir root directory",
    )
    warnings.showwarning = simple_warning(parser.prog)

    # Locate and load sub-commands
    command_list = commands()
    if len(command_list) > 0:
        subparsers = parser.add_subparsers(
            title="subcommands", metavar="SUBCOMMAND"
        )
        for command in command_list:
            command.add_subparser(subparsers)

    args = parser.parse_args(argv)

    # Run command
    try:
        if "func" in args:
            args.func(args)
        else:
            parse_maildirs(Path(args.mail_root))
    except Exception as err:
        if "DEBUG" in os.environ:
            logging.error(err, exc_info=True)
        else:
            die(f"{err}")
        sys.exit(1)
