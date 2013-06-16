mov
===

With **mov** you can browse your movie collection via a command-line interface.

**mov** expects your movies directory to look like this:

    root_dir
    ├── The Godfather
    |   └── The Godfather.mkv
    └── The Big Lebowski
        └── The Big Lebowski.mkv

Here *root_dir* just stands for the name of the root directory, which doesn't
matter. However, every top-level subdirectory is treated as a directory
containing a movie and the names of movies (in **mov**) are based on the name
of these subdirectories so it is important that they are carefully named.

## Setup

Simply clone the repository and create a symbolic link to mov.py in /usr/bin:

    git clone git@github.com:hph/mov.git && cd mov
    sudo ln -s mov.py /usr/bin/mov

Now you can create a database for these movies:

    $ mov create root_dir

## Usage

Run `mov -h` to learn more:

    Usage:
      mov create [options] DIRECTORY ...
      mov ls [options] [PATTERN]
      mov play [options] [PATTERN]
      mov -h | --help
      mov --version

    Commands:
      create               Create a new database with information about the films
                           in the specified directory or directories.
      ls                   List movies and relevant metadata optionally only
                           showing those that match a specified pattern.
      play                 Open matching movie with a media player.

    Options:
      --database=DATABASE  Database to save film metadata [default: mov.db].
      --name               Only show movie names when listing movies.
      --player=PLAYER      Media player to open movies with [default: vlc].
      --strict             Only list exact matches.
      -h, --help           Show this help message and exit.
      --version            Show version.
