from internetarchive.session import ArchiveSession
from internetarchive.search import Search
from internetarchive import get_item
import json, sys
import os
import shutil
import random
import string

SEARCH_QUERY = ''
MAX_MB_FILE = 10 * 1000000
FILE_DIR = './kasette/'

s = ArchiveSession()

def output(str):
    sys.stdout.write("\r%s" % str)
    sys.stdout.flush()

def reset_folder(directory):
    shutil.rmtree(directory, ignore_errors=True)

    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
        output('loaded kasette')
    except OSError:
        output('could not create kasette')

    return True

output('Tuning …')

reset_folder(FILE_DIR)

queries = []

for x in range(1,10):
    queries.append('%s %s' % (SEARCH_QUERY, random.choice(string.ascii_letters)))

for query in queries:
    search = Search(s, '(subject:%s OR title:%s AND mediatype:(audio) AND item_size:[0 TO "%s"])' % (SEARCH_QUERY, SEARCH_QUERY, MAX_MB_FILE))

    for result in search:
        item = get_item(result['identifier'])

        output('Found %s' % result['identifier'])

        files = item.files
        metadata = item.metadata

        for file in files:
            name = file['name'].lower()

            output('listening to %s' % name)

            if 'MP3' in file['format']:
                output('recording %s' % name)

                f = item.get_file(file['name'])
                f.download(FILE_DIR + name)

                break
