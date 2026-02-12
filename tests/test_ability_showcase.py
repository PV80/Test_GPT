import json
import subprocess
import sys
import unittest

import ability_showcase as m


class AbilityShowcaseTests(unittest.TestCase):
    def test_normalize_words(self):
        self.assertEqual(m.normalize_words("Hello, HELLO it's me!"), ["hello", "hello", "it's", "me"])

    def test_fibonacci_values(self):
        self.assertEqual(m.fibonacci(0), 0)
        self.assertEqual(m.fibonacci(1), 1)
        self.assertEqual(m.fibonacci(10), 55)

    def test_fibonacci_negative_raises(self):
        with self.assertRaises(ValueError):
            m.fibonacci(-1)

    def test_analyze_text(self):
        result = m.analyze_text("One fish two fish red fish blue fish", 8)
        self.assertEqual(result.word_count, 8)
        self.assertEqual(result.unique_words, 5)
        self.assertEqual(result.most_common_words[0], ["fish", 4])
        self.assertEqual(result.fibonacci_value, 21)

    def test_cli_outputs_json(self):
        output = subprocess.check_output(
            [sys.executable, "ability_showcase.py", "alpha beta alpha", "--fib", "7"], text=True
        )
        parsed = json.loads(output)
        self.assertEqual(parsed["word_count"], 3)
        self.assertEqual(parsed["fibonacci_value"], 13)


if __name__ == "__main__":
    unittest.main()
