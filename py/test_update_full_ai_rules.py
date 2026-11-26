"""Offline publication/failure tests; no subscriptions, credentials or network."""
import json
from pathlib import Path
import tempfile
import unittest

import update_full_ai_rules as updater

class UpdateTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        config = self.root / updater.OVERRIDES_PATH
        config.parent.mkdir(parents=True)
        config.write_text((updater.ROOT / updater.OVERRIDES_PATH).read_text(encoding='utf-8'), encoding='utf-8')
        self.sources = {}
        for name, (_, minimum, required) in updater.SOURCES.items():
            values = ['+.' + host for host in required]
            values += [f'test-{i}.ai-fixture.example.net' for i in range(max(minimum, 60))]
            self.sources[name] = updater.render(sorted(set(values)), 'offline test fixture')
        updater.publish(self.root, updater.prepare(self.root, self.sources.__getitem__))
        self.before = self.snapshot()

    def snapshot(self):
        return {str(path.relative_to(self.root)): path.read_bytes() for path in self.root.rglob('*.yaml')}

    def attempt(self, fetch):
        updater.publish(self.root, updater.prepare(self.root, fetch))

    def test_idempotent_and_manual_additions_survive(self):
        self.assertEqual(updater.publish(self.root, updater.prepare(self.root, self.sources.__getitem__)), [])
        values = updater.parse_payload((self.root / 'rule/ChatGPT_Domain.yaml').read_text())
        self.assertIn('cdn.openaimerge.com', values)
        updater.check(self.root)

    def test_download_failure_keeps_entire_published_batch(self):
        def fetch(name):
            if name == 'anthropic':
                raise OSError('synthetic upstream failure')
            return self.sources[name]
        with self.assertRaises(OSError):
            self.attempt(fetch)
        self.assertEqual(self.before, self.snapshot())

    def test_unsafe_scope_keeps_published_batch(self):
        self.sources['google-gemini'] += '  - +.googleapis.com\n'
        with self.assertRaises(ValueError):
            self.attempt(self.sources.__getitem__)
        self.assertEqual(self.before, self.snapshot())

    def test_domain_loss_requires_review(self):
        _, minimum, required = updater.SOURCES['openai']
        values = ['+.' + host for host in required] + [f'short-{i}.example.net' for i in range(minimum)]
        self.sources['openai'] = updater.render(values, 'synthetic truncated upstream')
        with self.assertRaisesRegex(ValueError, '30%'):
            self.attempt(self.sources.__getitem__)
        self.assertEqual(self.before, self.snapshot())

    def test_html_instead_of_yaml_keeps_published_batch(self):
        self.sources['bing'] = '<html>Temporary upstream error</html>'
        with self.assertRaises(ValueError):
            self.attempt(self.sources.__getitem__)
        self.assertEqual(self.before, self.snapshot())

    def test_scope_and_override_path_validation(self):
        self.assertEqual(updater.domain('+.bing'), '+.bing')
        for value in ['+.com', '+.google.com', '+.cloudflare.com', 'https://example.net', '../example.net']:
            with self.assertRaises(ValueError):
                updater.domain(value)
        path = self.root / updater.OVERRIDES_PATH
        path.write_text(json.dumps({'../escape.yaml': ['example.net']}))
        with self.assertRaises(ValueError):
            self.attempt(self.sources.__getitem__)
        self.assertEqual(self.before, self.snapshot())

if __name__ == '__main__':
    unittest.main()
