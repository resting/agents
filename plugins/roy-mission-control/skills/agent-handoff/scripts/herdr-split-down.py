#!/usr/bin/env python3
"""Create one Mission Control pane below the caller. Requires Python 3 and Herdr."""
import argparse
import os
from pathlib import Path
import subprocess
import sys


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--cwd', required=True, type=Path, help='Mission checkout directory')
    args = parser.parse_args()
    if os.environ.get('HERDR_ENV') != '1':
        print('Mission Control: run this from the captain inside Herdr.', file=sys.stderr)
        return 1
    directory = args.cwd.resolve()
    if not directory.is_dir():
        parser.error(f'Mission directory does not exist: {directory}')
    try:
        # Keep Herdr's JSON and exit status intact. Never retry a split or change direction.
        return subprocess.run([
            'herdr', 'pane', 'split', '--current', '--direction', 'down',
            '--cwd', str(directory), '--no-focus',
        ], check=False).returncode
    except OSError as error:
        print(f'Mission Control: could not run Herdr: {error}', file=sys.stderr)
        return 1


if __name__ == '__main__':
    sys.exit(main())
