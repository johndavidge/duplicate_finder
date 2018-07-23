import subprocess
import unittest


class TestDuplicateFinder(unittest.TestCase):
    def test_help(self):
        process = subprocess.Popen(['python', 'duplicate_finder.py', '-h'],
                                   stdout=subprocess.PIPE)
        output, error = process.communicate()
        help_string = 'usage: python duplicate_finder.py <directory>'
        self.assertIsNone(error)
        self.assertIn(help_string, output.decode('utf-8'))

    def test_syntax_error(self):
        try:
            process = subprocess.check_output(['python',
                                               'duplicate_finder.py'])
        except subprocess.CalledProcessError as error:
            self.assertEqual(error.returncode, 2)
            self.assertIn('takes exactly 1 argument',
                          error.output.decode('utf-8'))
            return

        self.assertTrue(False)

    def test_invalid_directory(self):
        try:
            process = subprocess.check_output(['python',
                                               'duplicate_finder.py',
                                               './fake_directory'])
        except subprocess.CalledProcessError as error:
            self.assertEqual(error.returncode, 1)
            self.assertIn('Invalid directory', error.output.decode('utf-8'))
            return

        self.assertTrue(False)

    def test_empty_directory(self):
        process = subprocess.Popen(['python',
                                    'duplicate_finder.py',
                                    './test_directory/empty_directory'],
                                   stdout=subprocess.PIPE)
        output, error = process.communicate()
        self.assertIsNone(error)
        self.assertIn('No duplicates found', output.decode('utf-8'))

    def test_valid_directory(self):
        process = subprocess.Popen(['python',
                                    'duplicate_finder.py',
                                    './test_directory'],
                                   stdout=subprocess.PIPE)
        output, error = process.communicate()
        output = output.decode('utf-8')
        self.assertIsNone(error)
        self.assertIn('Found 2 group(s)', output)

        for i in range(1, 5):
            self.assertIn('duplicate_%s' % i, output)

        self.assertNotIn('different', output)


if __name__ == '__main__':
    unittest.main()
