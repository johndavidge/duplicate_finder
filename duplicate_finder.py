import hashlib
import os
import sys

# Limit hash chunks to 64kb
BUFFER_SIZE = 65536


def help():
    print('A simple utility for finding groups of duplicate files in a given '
          'directory tree.')
    print('')
    print('usage: python duplicate_finder.py <directory>')
    print('')
    print('Where <directory> is a relative or absolute path to the root of '
          'the directory tree.')


def main(argv):
    if '-h' in argv:
        help()
        return

    if len(argv) != 2:
        print('duplicate_finder takes exactly 1 argument. %s given.'
              % (len(argv) - 1))
        print("Use 'python duplicate_finder.py -h' for help.")
        sys.exit(2)

    dir_path = argv[1]
    if not os.path.isdir(dir_path):
        print('Invalid directory: %s' % dir_path)
        sys.exit(1)

    hashed_files = {}
    uninspected_files = []
    for root, directories, filenames in os.walk(dir_path):
        for filename in filenames:
            # Create a fresh md5 instance for each file
            md5 = hashlib.md5()
            file_path = os.path.join(root, filename)
            try:
                with open(file_path, 'rb') as f:
                    # Read the data in, chunk by chunk
                    # This should prevent large files eating up too much memory
                    while True:
                        data = f.read(BUFFER_SIZE)
                        if not data:
                            break
                        md5.update(data)
                    # Generate a hash of the file contents
                    # Files with identical contents will produce
                    # identical hashes.
                    file_hash = md5.hexdigest()
                    # Store filepaths grouped by hash
                    if file_hash in hashed_files:
                        hashed_files[file_hash].append(file_path)
                    else:
                        hashed_files[file_hash] = [file_path]
            except Exception:
                # This file requires elevated permissions or is otherwise
                # unopenable. Skip it, but make a note.
                uninspected_files.append(file_path)

    duplicates = 0
    for file_hash, file_paths in hashed_files.items():
        if len(file_paths) > 1:
            duplicates += 1
            print('========== Duplicate files: ==========')
            for file_path in file_paths:
                print(file_path)

    if len(uninspected_files) > 0:
        print('========== %s file(s) could not be inspected: =========='
              % len(uninspected_files))
        for file_path in uninspected_files:
            print(file_path)

    if duplicates == 0:
        print('No duplicates found.')
    else:
        print('========== Found %s group(s) of '
              'duplicate files ==========' % duplicates)


if __name__ == '__main__':
    main(sys.argv)
