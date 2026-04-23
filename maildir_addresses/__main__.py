"""maildir-addresses: Launcher.

© Reuben Thomas <rrt@sc3d.org> 2026.

Released under the GPL version 3, or (at your option) any later version.
"""

import re
import sys

from maildir_addresses import main


sys.argv[0] = re.sub(r"__main__.py$", "maildir_addresses", sys.argv[0])
main()
