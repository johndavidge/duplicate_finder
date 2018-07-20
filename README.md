# duplicate_finder
A simple python utility for finding files with duplicate contents in a given directory tree.

Only uses modules from the standard library.

## Setup

First, clone the project to you local machine and cd into the project directory:

```
$ git clone https://github.com/johndavidge/duplicate_finder.git
$ cd duplicate_finder
```

## Usage

To search for duplicate files, simply use:

```
$ python duplicate_finder.py <directory>
```

Where `<directory>` is a relative or absolute path to the root of the directory tree you wish to search.

For example:

```
$ python duplicate_finder.py test_directory/
========== Duplicate files: ==========
test_directory/duplicate_1.txt
test_directory/more_test_files/duplicate_2.txt
========== Duplicate files: ==========
test_directory/more_test_files/duplicate_3.txt
test_directory/more_test_files/duplicate_4.txt
========== Found 2 group(s) of duplicate files ==========
```

For help, use the `-h` option:

```
$ python duplicate_finder.py -h
A simple utility for finding groups of duplicate files in a given directory tree.

usage: python duplicate_finder.py <directory>

Where <directory> is a relative or absolute path to the root of the directory tree.
```

## Testing

Tests can be found in `test_duplicate_finder.py`.

Tests are written with `unittest` and make use of the `subprocess` module to invoke cli commands.

To run the tests, use:

```
$ python test_duplicate_finder.py
.....
----------------------------------------------------------------------
Ran 5 tests in 0.073s

OK
```
