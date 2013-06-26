mov
===

**mov** is a command-line application to browse your movie collection.

* List movies: `mov ls | less`
* List specific movies: `mov ls the godfather`
* Play a movie: `mov play the godfather`

## Setup

Run the following commands to download and install **mov**. You may be required
to enter your password.

    bash <(wget -qO- https://raw.github.com/hph/mov/master/setup.sh)

## Usage

We will assume that `~/Movies` is a directory containing subdirectories,
themselves containing movies and related files, e.g., running `tree ~/Movies`
should show something like this:
    
    ~/Movies
    ├── 12 Angry Men
    │   └── 12 Angry Men.mkv
    ├── 2001 - A Space Odyssey
    │   └── 2001 - A Space Odyssey.mkv
    ...

First you will have to create a database of your movies:

    mov create ~/Movies

Now watch a movie:

    mov play odyssey

Run `mov -h` to show what else you can do.

## Unix trickery

**mov** is desinged in such a way as to be usable with standard Unix utilities.

* Run `mov ls | less` to browse a large number of movies more comfortably. You
  can use `j` to go down and `k` to go up. Use `/pattern` to search for a
  movie.
* Run `mov ls --name | wc -l` to count the number of movies in your database.
* Run `mov ls | grep pattern` to search for "pattern".
* Run `mov ls -S --prefix G | awk '{s += $1} END {print s}'` to show the
  total size of the movie collection in gibibytes.

## Available commands and options

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
      --prefix=PREFIX      Size prefix, one of none, k, M, G or T [default: None].
      --player=PLAYER      Media player to open movies with [default: vlc].
      -h, --help           Show this help message and exit.
      --version            Show version.

## To do

* Improve the way data is displayed.
* Use IMDbPy to retrieve information about movies.
* Allow marking movies as seen or unseen.
* Add rating movies.
* Implement a watchlist (mark as "watch this").
* Use SQLAlchemy to build a movies model for a better API.
* Search for and get magnet to download movies.
* Show statistics: number of movies, total size, formats, etc.
