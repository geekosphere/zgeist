# Zeitgeist

## Setup

### Database

In short you need postgres with some way of authentication configured,
a zeitgeist specific user and (atleast) two databases for production
and testing. Change `conf/local.yml` to your database config. (see
`conf/local.yml.sample` for an example.

Locate postgres cluster directory / data directory:

```
% sudo su postgres -c "psql -c \"SHOW data_directory\""
   data_directory    
---------------------
 /var/lib/pgsql/data
(1 row)
```

Allow password/md5 authentication:

```
% sudo cat /var/lib/pgsql/data/pg_hba.conf
local   all     postgres                   trust
local   all     all                        md5
host    all     all         0.0.0.0/0      md5
host    all     all         ::/128         md5
host    all     all         ::1/128        md5
```

Create user and databases:

```
sudo su postgres -c psql
postgres=# CREATE USER zg WITH PASSWORD 'changeme';
postgres=# CREATE DATABASE zg;
postgres=# CREATE DATABASE zg_test;
postgres=# GRANT ALL PRIVILEGES ON DATABASE zg TO zg;
postgres=# GRANT ALL PRIVILEGES ON DATABASE zg_test TO zg;
```

Change local site configuration (`conf/local.yml`):

```yaml
--- # example local configuration
production:
  database:
    uri: 'postgresql://zg:changeme@localhost/zg'
  [...]
development:
  database:
    uri: 'postgresql://zg:changeme@localhost/zg'
  [...]
test:
  database:
    uri: 'postgresql://zg:changeme@localhost/zg_test'
  [...]
```

### Celery

Celery in production depends on a message queue backend server, such as
rabbitmq, consult the celery documentation on how to set this up. You
might need to change the `celery` config option.

You also need to start a celery worker process like this:

```
celery worker -A zg.app.celery
```

To change to your virtualenv and run the worker in one command use
something like this:

```
/home/apoc/.virtualenvs/zgeist/bin/celery worker --workdir \
    /home/apoc/projects/python/zgeist -A zg.app.celery
```

Sample supervisord config:

```
[program:zg-celery]
numprocs=1
directory=/home/apoc/projects/python/zgeist
environment=ENV=production
command=/home/apoc/.virtualenvs/zgeist/bin/celery worker -A zg.app.celery
```

