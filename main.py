from __future__ import print_function, unicode_literals
import sys

from search import Search, Paper

try:
    import ConfigParser  # Python 2
except:
    import configparser as ConfigParser  # Python 3


def read_from_config(term_or_depth='term'):
    try:
        config = ConfigParser.ConfigParser()
        config.read('config.cfg')
        response = config.get('Search', term_or_depth)
    except ConfigParser.NoSectionError:
        print('Define initial search term and depth in a "config.cfg" file.')
        response = ''
    return response


def read_from_cli(term_or_depth='term'):
    index = 1 if term_or_depth == 'term' else 2
    if len(sys.argv) < 1 + index:
        response = ''
    else:
        response = sys.argv[index]
    return response


if __name__ == '__main__':
    term = read_from_cli('term') or read_from_config('term')
    depth = int(read_from_cli('depth')
                or read_from_config('depth'))
    print(term, depth)
    exit()

    search = Search(term)

    for rec in search.records:
        print(rec.au, rec.edat)

    print('term', search.term)
    print('web_env', search.web_env)
    print('count', search.count)
    print('query_key', search.query_key)
