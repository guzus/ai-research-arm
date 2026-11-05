import copy
import tempfile
import unittest
from pathlib import Path

from verify_chubby_canary import verify


class ChubbyCanaryTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.source = Path(self.tmp.name) / 'input.txt'
        self.output = Path(self.tmp.name) / 'output.txt'
        self.source.write_text('chubby-canary-random-challenge\n')
        self.output.write_text(self.source.read_text())
        self.model = 'openrouter/deepseek/deepseek-v4.1-flash-1017'
        self.objects = [
            {'type': 'assistant', 'message': {'model': self.model, 'content': [
                {'type': 'tool_use', 'id': 'read-1', 'name': 'Read',
                 'input': {'file_path': str(self.source)}}]}},
            {'type': 'user', 'message': {'content': [
                {'type': 'tool_result', 'tool_use_id': 'read-1', 'content': self.source.read_text()}]}},
            {'type': 'assistant', 'message': {'model': self.model, 'content': [
                {'type': 'tool_use', 'id': 'write-1', 'name': 'Write',
                 'input': {'file_path': str(self.output), 'content': self.source.read_text()}}]}},
            {'type': 'user', 'message': {'content': [
                {'type': 'tool_result', 'tool_use_id': 'write-1', 'content': 'File written'}]}},
            {'type': 'result', 'subtype': 'success', 'is_error': False,
             'modelUsage': {self.model: {'inputTokens': 100, 'outputTokens': 10}}},
        ]

    def check(self, objects=None):
        verify(objects if objects is not None else self.objects, self.model, self.source, self.output)

    def test_completed_tool_roundtrip(self):
        self.check()

    def test_accepts_provider_native_model_identity(self):
        native = self.model.split('/', 1)[1]
        for obj in self.objects:
            if obj.get('type') == 'assistant':
                obj['message']['model'] = native
        self.objects[-1]['modelUsage'] = {native: {}}
        self.check()

    def test_rejects_failed_incomplete_or_unattributed_execution(self):
        variants = [self.objects[:-1], [], self.objects[2:]]
        for field, value in [('is_error', True), ('subtype', 'error_max_turns')]:
            objects = copy.deepcopy(self.objects)
            objects[-1][field] = value
            variants.append(objects)
        objects = copy.deepcopy(self.objects)
        objects[0]['message']['model'] = 'claude-sonnet-5-5'
        variants.append(objects)
        for objects in variants:
            with self.subTest(objects=objects), self.assertRaises(ValueError):
                self.check(objects)

    def test_rejects_uncompleted_or_errored_tool(self):
        for index in [1, 3]:
            with self.subTest(index=index), self.assertRaises(ValueError):
                self.check(self.objects[:index] + self.objects[index + 1:])
        self.objects[1]['message']['content'][0]['is_error'] = True
        with self.assertRaises(ValueError):
            self.check()

    def test_rejects_wrong_content_or_symlink(self):
        self.output.write_text('old-result\n')
        with self.assertRaises(ValueError):
            self.check()

    def test_exact_copy_rejects_newline_conversion(self):
        self.output.write_bytes(self.source.read_bytes().replace(b'\n', b'\r\n'))
        with self.assertRaises(ValueError):
            self.check()
        self.output.unlink()
        self.output.symlink_to(self.source)
        with self.assertRaises(ValueError):
            self.check()


if __name__ == '__main__':
    unittest.main()
