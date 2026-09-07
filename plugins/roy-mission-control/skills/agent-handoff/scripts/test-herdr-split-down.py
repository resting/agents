#!/usr/bin/env python3
"""Exercise the split helper using a fake CLI; never connect to a Herdr session."""
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


HELPER = Path(__file__).resolve().with_name('herdr-split-down.py')


class SplitDownTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix='rmc-split-')
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.project = self.root / 'project with spaces; $(touch unexpected)'
        self.project.mkdir()
        self.log = self.root / 'calls.jsonl'
        self.cli = self.root / 'herdr'
        self.cli.write_text(f'#!{sys.executable}\n' + '''import json, os, sys
with open(os.environ['RMC_TEST_LOG'], 'a') as log:
    log.write(json.dumps(sys.argv[1:]) + '\\n')
code = int(os.environ.get('RMC_TEST_EXIT', '0'))
print('fixture error' if code else '{"result":{"pane":{"pane_id":"fixture:p42"}}}',
      file=sys.stderr if code else sys.stdout)
sys.exit(code)
''')
        self.cli.chmod(0o755)
        # PATH contains only the fake CLI. HERDR_ENV here cannot reach a real session.
        self.env = {'PATH': str(self.root), 'HERDR_ENV': '1', 'RMC_TEST_LOG': str(self.log)}

    def run_helper(self, *args):
        return subprocess.run(
            [sys.executable, str(HELPER), '--cwd', str(self.project), *args],
            env=self.env, capture_output=True, text=True, check=False,
        )

    def calls(self):
        return [json.loads(line) for line in self.log.read_text().splitlines()]

    def test_split_down_preserves_caller_directory_focus_and_returned_id(self):
        result = self.run_helper()
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(self.calls(), [[
            'pane', 'split', '--current', '--direction', 'down',
            '--cwd', str(self.project.resolve()), '--no-focus',
        ]])
        self.assertEqual(json.loads(result.stdout)['result']['pane']['pane_id'], 'fixture:p42')

    def test_direction_cannot_be_overridden(self):
        result = self.run_helper('--direction', 'right')
        self.assertEqual(result.returncode, 2)
        self.assertFalse(self.log.exists())

    def test_outside_herdr_never_calls_cli(self):
        self.env.pop('HERDR_ENV')
        result = self.run_helper()
        self.assertEqual(result.returncode, 1)
        self.assertIn('inside Herdr', result.stderr)
        self.assertFalse(self.log.exists())

    def test_missing_directory_never_calls_cli(self):
        result = self.run_helper('--cwd', str(self.root / 'missing'))
        self.assertEqual(result.returncode, 2)
        self.assertFalse(self.log.exists())

    def test_cli_failure_is_preserved_without_retry_or_right_fallback(self):
        self.env['RMC_TEST_EXIT'] = '1'
        result = self.run_helper()
        self.assertEqual(result.returncode, 1)
        self.assertEqual(result.stderr, 'fixture error\n')
        self.assertEqual(result.stdout, '')
        self.assertEqual(len(self.calls()), 1)
        self.assertNotIn('right', self.calls()[0])

    def test_missing_cli_is_reported_without_traceback(self):
        self.cli.unlink()
        result = self.run_helper()
        self.assertEqual(result.returncode, 1)
        self.assertIn('could not run Herdr', result.stderr)
        self.assertNotIn('Traceback', result.stderr)


if __name__ == '__main__':
    unittest.main()
