import subprocess
import unittest


class TestDuplicateFinder(unittest.TestCase):
    def test_help(self):
        process = subprocess.Popen(['python', 'duplicate_finder.py', '-h'],
                                   stdout=subprocess.PIPE)
        output, error = process.communicate()
        help_string = 'usage: python duplicate_finder.py <directory>'
        assert error is None
        assert help_string in output.decode('utf-8')

    def test_syntax_error(self):
        try:
            process = subprocess.check_output(['python',
                                               'duplicate_finder.py'])
        except subprocess.CalledProcessError as error:
            assert error.returncode == 2
            assert 'takes exactly 1 argument' in error.output.decode('utf-8')
            return

        assert false

    def test_invalid_directory(self):
        try:
            process = subprocess.check_output(['python',
                                               'duplicate_finder.py',
                                               './fake_directory'])
        except subprocess.CalledProcessError as error:
            assert error.returncode == 1
            assert 'Invalid directory' in error.output.decode('utf-8')
            return

        assert false

    def test_empty_directory(self):
        process = subprocess.Popen(['python',
                                    'duplicate_finder.py',
                                    './test_directory/empty_directory'],
                                   stdout=subprocess.PIPE)
        output, error = process.communicate()
        assert error is None
        assert 'No duplicates found' in output.decode('utf-8')

    def test_valid_directory(self):
        process = subprocess.Popen(['python',
                                    'duplicate_finder.py',
                                    './test_directory'],
                                   stdout=subprocess.PIPE)
        output, error = process.communicate()
        output = output.decode('utf-8')
        assert error is None
        assert 'Found 2 group(s)' in output
        assert 'duplicate_1' in output
        assert 'duplicate_2' in output
        assert 'duplicate_3' in output
        assert 'duplicate_4' in output
        assert 'different' not in output


if __name__ == '__main__':
    unittest.main()
