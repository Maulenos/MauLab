from datetime import datetime, timezone
import unittest
from unittest.mock import patch
from scripts.update_activity import read_commits, render_activity, replace_activity, START, END


class ActivityTests(unittest.TestCase):
    def test_bot_refresh_does_not_count_as_progress(self):
        log = ('a' * 40 + '\t2026-10-31T12:00:00+00:00\tchore: refresh repository activity\n'
               + 'b' * 40 + '\t2026-10-30T12:00:00+00:00\tAdd runbook\n')
        with patch('scripts.update_activity.subprocess.check_output', return_value=log):
            commits = read_commits()
        self.assertEqual(len(commits), 1)
        self.assertEqual(commits[0][2], 'Add runbook')

    def test_quiet_day_preserves_historical_changes(self):
        block = render_activity([('a' * 40, datetime(2026, 10, 1, tzinfo=timezone.utc), 'Older work')],
                                datetime(2026, 10, 31, 13, 17, tzinfo=timezone.utc))
        self.assertIn('No new substantive commits', block)
        self.assertIn('Older work', block)
        self.assertIn('08:17 CDT', block)

    def test_commit_subject_cannot_inject_links_or_html(self):
        now = datetime(2026, 10, 31, tzinfo=timezone.utc)
        block = render_activity([('a' * 40, now, '[fake](https://example.com) <img>')], now)
        self.assertNotIn('[fake](', block)
        self.assertNotIn('<img>', block)
        self.assertIn('1 substantive commit in', block)

    def test_update_is_scoped_and_repeatable(self):
        original = f'Keep intro\n{START}\nold\n{END}\nKeep footer'
        expected = f'Keep intro\n{START}\nnew\n{END}\nKeep footer'
        self.assertEqual(replace_activity(original, 'new'), expected)
        self.assertEqual(replace_activity(expected, 'new'), expected)

    def test_missing_duplicate_or_reversed_markers_fail(self):
        for content in ['', START + START + END, END + START]:
            with self.subTest(content=content), self.assertRaises(ValueError):
                replace_activity(content, 'new')

    def test_winter_timezone_and_empty_history(self):
        block = render_activity([], datetime(2026, 12, 1, 13, 17, tzinfo=timezone.utc))
        self.assertIn('07:17 CST', block)
        self.assertIn('No substantive commits found', block)


if __name__ == '__main__':
    unittest.main()
