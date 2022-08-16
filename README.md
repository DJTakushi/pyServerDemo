# Takushi
Demonstration server for python project.  Created to explore using Heroku for hosting python (Django) projects.

## Setting up Database
Django is configured to use python's included SQLite database system.  This default behavior is wonderful for locally hosting, but it's unsuitable for production.  I intended to host this on Heroku, which has a free version of a PostgreSQL database that is recommended for production.

[Djangocentral has a great article on using 'PostgreSQL with Django'](https://djangocentral.com/using-postgresql-with-django/).  I'm including my own instructions here for convenience, customization, and learning-by-documenting:

### 1 Install PostgreSQL
I'm using Windows and I prefer winget to click-through-installers.  Use the later if you dare, but I use:

`winget install -e --id PostgreSQL.PostgreSQL`

(This seems to install an unfortunately outdated version of the GUI application, but the database itself is okay.)

### 2 Log in to PostgreSQL
Log in to PostgreSQL with the default `postgres` user.  When prompted, enter the default password (`postgres`):

`psql -U postgres`

### 3 Create the server's database
`CREATE DATABASE takushi;`

### 4 Create the server's user
`CREATE USER takushi_u WITH ENCRYPTED PASSWORD 'takushi_u_Password';`

### 5 Set recommended parameters
`ALTER ROLE takushi_u SET client_encoding TO 'utf8';`

`ALTER ROLE takushi_u SET default_transaction_isolation TO 'read committed';`

`ALTER ROLE takushi_u SET timezone TO 'UTC';`

### 6 Grant permissions to user
`GRANT ALL PRIVILEGES ON DATABASE takushi TO takushi_u;`

psql can be exited with `\q`

If you want to log in to PostgreSQL with this user, use the command:

`psql -U takushi_u -d takushi`

Enter the password when prompted.

### 7 Create migrations in database
`py manage.py migrate`

You should now be able to run your server with either:
- `py manage.py runserver`
- `heroku local -f Procfile.windows` (`heroku local` if your Unix)

# dblog
dblog was written to be served on github pages and I'd like to keep that system in place for backwards compatibility/precedence.

To integrate it to this site though, it seems as though the best option is to generate the static pages on my machine and add these derived files to version control.  Since Jekyll is a Ruby Gem and not a python file, this seems like it can't be offloaded to a remove server.  Life is truly suffering.

## Installing Jekyll

## Install Ruby (Windows)
`winget install -e --id RubyInstallerTeam.Ruby`
Broken.  Following official documentation [https://jekyllrb.com/docs/installation/windows/](https://jekyllrb.com/docs/installation/windows/).

Use the GUI installer at[https://rubyinstaller.org/](https://rubyinstaller.org/).

## Install jekyll
`gem install jekyll bundler`

Confirm successful installation with `jekyll -v`

Note that you may have to install several other gems.  I had to install:
- `wdm`
- `webrick`
- `jekyll-mentions`
- `github-pages`

This probably works better on Linux.

## Build static site
`bundle exec jekyll build --layouts djangoTemplates -d dblogDjango`
- `--layouts djangoTemplates` will use django-specific/generated templates.  This is done to allow gitHub pages hosting to continue to use the native content in `_layouts`.  In the future these should be reconciled.
- `-d dblogDjango` will set the destination in a new folder.  This is to protect the native `_site` for gitHub pages.  As above, this could be reconciled/simplified in the future.

## Create SuperUser
Per [https://docs.djangoproject.com/en/4.0/topics/auth/default/#creating-users](https://docs.djangoproject.com/en/4.0/topics/auth/default/#creating-users), create a superuser by using:

`[heroku run]` `python manage.py createsuperuser --username=joe --email=joe@example.com`

TODO: This could be done in an automatic script, but since it doesn't work in an `AppConfig`'s `ready()` function (database loading problem(?)), doing it by hand will suffice for now.

## Code Coverage

#### Setup
Install [coverage.py](https://coverage.readthedocs.io/en/6.4.3/) with

`pip install coverage`

#### Run Tests
`coverage run --source='.' manage.py test`

#### View Test Results in Console
`coverage report`

#### HTML Reports
`coverage html`
