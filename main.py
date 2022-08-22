import os
from collections import defaultdict
import hashlib
import sys

md5 = hashlib.md5()

# hold our files with file size as key and a list of paths as values
file_map = defaultdict(list)


# this algorithm is predicated on the fact that duplicate files will have same size
def build_file_map(cur_path):
    dir_contents = os.listdir(cur_path)

    for content in dir_contents:
        content_path = os.path.join(cur_path, content)
        # if the path is a file, get the file size and add it to the file map
        if os.path.isfile(content_path):
            with open(content_path, 'rb') as file:
                file_size = os.path.getsize(content_path)
                file_map[file_size].append(content_path)
        else:
            # if the path is a folder, recursively traverse the folder
            build_file_map(content_path)


def delete_dupes():
    file_hashes = set()

    for files in file_map.values():
        # no need to create hashes for entries with less than 2 values because there are no duplicates
        if len(files) < 2:
            continue

        for file in files:
            with open(file, 'rb') as cur_file:
                # read the first 1000 bytes of the file and hash the data
                data = cur_file.read(1024)
                hashed_data = hashlib.md5(data).hexdigest()
                # duplicates will have matching hashes for their first 1000 bytes in addition to being the same size
                if hashed_data in file_hashes:
                    os.remove(file)
                else:
                    file_hashes.add(hashed_data)


if __name__ == '__main__':
    pathname = sys.argv[1]
    build_file_map(pathname)
    delete_dupes()
