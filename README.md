mov
===

With **mov** you can browse your movie collection via a command-line interface.

**mov** expects your movies directory to look something like this:

    root_dir
    ├── The Godfather
    |   └── The Godfather.mkv
    └── The Big Lebowski
        └── The Big Lebowski.mkv

Here *root_dir* just stands for the name of the root directory, which doesn't
matter to **mov**. However, every top-level subdirectory (e.g., The Godfather
and The Big Lebowski) is treated as a directory containing a movie and the
names of movies in **mov**) are based on the name of these subdirectories so
it is important that they are carefully named.

## Setup

You must install docopt if you haven't already:

    pip install docopt

Now clone the repository, move it to your home directory, make it executable
and create a symbolic link to mov.py in /usr/bin/mov:

    git clone git@github.com:hph/mov.git
    mv mov/ ~/.mov
    chmod +x ~/.mov/mov.py
    sudo ln -s ~/.mov/mov.py /usr/bin/mov

Create a database for the movies in the example above:

    mov create root_dir

The database will be created in your home directory (~/.mov.db) if you don't
specify it explicitly with the `--database` option.

## Usage

As the program is still under development, some features have not yet been
fully developed. You can find out what can be done at this point in time by
running `mov -h`:

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

## Unix trickery

**mov** is desinged in such a way as to be usable with standard Unix utilities.

* Run `mov ls | less` to browse a large number of movies more comfortably. You
  can use `j` to go down and `k` to go up. Use `/pattern` to search for a
  movie.
* Run `mov ls --name | wc -l` to count the number of movies in your database.
* Run `mov ls | grep pattern` to search for "pattern".

## To do

* Improve the way data is displayed.
* Use IMDbPy to retrieve information about movies.
* Allow marking movies as seen or unseen.
* Add rating movies.
* Implement a watchlist (mark as "watch this").
* Use SQLAlchemy to build a movies model for a better API.
* Search for and get magnet to download movies.
* Show statistics: number of movies, total size, formats, etc.
