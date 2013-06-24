#!/usr/bin/env python
#coding=utf8

"""
Usage:
  mov create [options] DIRECTORY ...
  mov update [options] DIRECTORY ...
  mov destroy [options]
  mov ls [options] [PATTERN ...]
  mov play [options] [PATTERN ...]
  mov -h | --help
  mov --version

Commands:
  create               Create a new database with information about the films
                       in the specified directory or directories.
  update               Update an existing database. Old items that are not
                       found are deleted.
  destroy              Destroy a database.
  ls                   List movies and relevant metadata optionally only
                       showing those that match a specified pattern.
  play                 Open the first matching movie with a media player.

Options:
  --database=DATABASE  Database to save film metadata [default: ~/.mov.db].
  --force              Do not prompt for a confirmation upon database
                       destruction.
  -s, --strict         Only show exact matches.
  -n, --name           Only show the name of the movie.
  -l, --location       Only show the location of the movie.
  -S, --size           Only show the size of the movie.
  -f, --files          Only show the files of the movie.
  --player=PLAYER      Media player to open movies with [default: vlc].
  -h, --help           Show this help message and exit.
  --version            Show version.
"""

__version__ = '0.0.1'

import os
import sqlite3

try:
    from docopt import docopt
except ImportError, error:
    exit('Error: {0}. Install it with "pip install docopt".'.format(error))


def get_size(path):
    '''Return the size of path in bytes if it exists and can be determined.'''
    size = os.path.getsize(path)
    for item in os.walk(path):
        for file in item[2]:
            size += os.path.getsize(os.path.join(item[0], file))
    return size


def local_data(path):
    """Return tuples of names, directories, total sizes and files. Each
       directory represents a single film and the files are the files contained
       in the directory, such as video, audio and subtitle files."""
    dirs = [os.path.join(path, item) for item in os.listdir(path)]
    names, sizes, files = zip(*[(dir.split('/')[-1], str(get_size(dir)),
                                 '##'.join([file for file in os.listdir(dir)]))
                                for dir in dirs])
    return zip(names, dirs, sizes, files)


def prefix_size(size, base=1024):
    '''Return size in B (bytes), kB, MB, GB or TB.'''
    for i, p in enumerate(['', 'ki', 'Mi', 'Gi', 'Ti']):
        if size < pow(base, i + 1):
            return '{0} {1}B'.format(round(float(size) / pow(base, i), 1), p)


def create():
    """Create a new database with information about the films in the specified
       directory or directories."""
    if not all(map(os.path.isdir, ARGS.directory)):
        exit('Error: One or more of the specified directories does not exist.')
    with sqlite3.connect(ARGS.database) as connection:
        connection.text_factory = str
        cursor = connection.cursor()
        cursor.execute('DROP TABLE IF EXISTS Movies')
        cursor.execute('''CREATE TABLE movies(name TEXT, path TEXT, size TEXT,
                          files BLOB)''')
        for dir in ARGS.directory:
            cursor.executemany('INSERT INTO Movies VALUES(?, ?, ?, ?)',
                               local_data(dir))


def update():
    """Update an existing database. Old items that are not found are
       deleted."""
    # Temporarily use the same method to create and update a database.
    return create


def destroy():
    """Destroy a database."""
    if not os.path.exists(ARGS.database):
        exit('Error: The database does not exist; you must create it first.')
    if ARGS.force:
        os.remove(ARGS.database)
    elif raw_input('Destroy {0} [y/n]? '.format(ARGS.database)) in ('y', 'Y'):
        os.remove(ARGS.database)


def ls():
    """List all items in the database in a predefined format."""
    if not os.path.exists(ARGS.database):
        exit('Error: The database does not exist; you must create it first.')
    with sqlite3.connect(ARGS.database) as connection:
        connection.text_factory = str
        cursor = connection.cursor()
        if ARGS.pattern:
            if not ARGS.strict:
                ARGS.pattern = '%{0}%'.format(ARGS.pattern)
            cursor.execute('SELECT * FROM Movies WHERE Name LIKE (?)',
                      [ARGS.pattern])
        else:
            cursor.execute('SELECT * FROM Movies')
        movies = [row for row in cursor]
    if ARGS.name:
        print '\n'.join([movie[0] for movie in movies])
    elif ARGS.location:
        print '\n'.join([movie[1] for movie in movies])
    elif ARGS.size:
        print '\n'.join([prefix_size(int(movie[2])) for movie in movies])
    elif ARGS.files:
        print '\n'.join([movie[3].split('##')[0] for movie in movies])
    else:
        for i, movie in enumerate(movies):
            print 'Name:\t\t{0}'.format(movie[0])
            print 'Location:\t{0}'.format(movie[1])
            print 'Size:\t\t{0}'.format(prefix_size(int(movie[2])))
            print 'Files:\t\t{0}'.format(', '.join(movie[3].split('##')))
            if not i == len(movies) - 1:
                print


def play():
    """Open the matched movie with a media player."""
    with sqlite3.connect(ARGS.database) as connection:
        connection.text_factory = str
        cursor = connection.cursor()
        if ARGS.pattern:
            if not ARGS.strict:
                ARGS.pattern = '%{0}%'.format(ARGS.pattern)
            cursor.execute('SELECT * FROM Movies WHERE Name LIKE (?)',
                           [ARGS.pattern])
            try:
                path = [row for row in cursor][0][1]
                replace_map = {' ': '\\ ', '"': '\\"', "'": "\\'"}
                for key, val in replace_map.iteritems():
                    path = path.replace(key, val)
                os.system('{0} {1} &'.format(ARGS.player, path))
            except IndexError:
                exit('Error: Movie not found.')


def main():
    # If the arguments are not valid (as defined in __doc__) the program exits.
    args_dict = docopt(__doc__, version='mov {0}'.format(__version__))
    global ARGS
    # Clean key names for later namespace use.
    ARGS = {arg.lower().replace('--', ''): args_dict[arg] for arg in args_dict}
    # Make arguments available in a namespace.
    ARGS = type('Namespace', (object,), ARGS)
    # Resolve ~ to the user's home directory if applicable.
    if ARGS.database[0] == '~':
        ARGS.database = os.path.expanduser('~') + ARGS.database[1:]
    if len(ARGS.pattern) > 1:
        ARGS.pattern = ' '.join(ARGS.pattern)
    elif len(ARGS.pattern):
        ARGS.pattern = ARGS.pattern[0]
    commands = ('create', 'update', 'destroy', 'ls', 'play')
    # Call the respective function for the command entered.
    locals()[[command for command in commands if args_dict[command]][0]]()


if __name__ == '__main__':
    main()
