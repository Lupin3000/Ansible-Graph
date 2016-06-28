# Ansible-Graph


With Ansible-Graph you create reports and graphs (_using Graphviz_) about your Ansible project structure (_Directories and Files_) and Ansible roles.

---

## Development Requirements

Required Python version:

- 2.7.x

Min. required libraries:

- pip (8.1.2)
- graphviz (0.4.10)
- pylint (_1.5.6 - optional_)
- bandit (_1.0.1 - optional_)

---

## Installation and usage

### Recommended option: (_virtualenv_)

```
# install virtualenv with dependencies
$ make env

# install only dependencies
$ make deps

# run pylint (optional)
$ make lint

# run bandit (optional)
$ make bandit

# remove virtualenv
$ make cleanenv
```

### Usage:

```
# show help
$ .env/bin/python -B ansible_graph.py --help

# run application
$ .env/bin/python -B ansible_graph.py <project> <configuration>
```

### Not-recommended option: (_system wide_)

```
# install system wide
$ sudo pip install -r requirements.txt

# show help
$ make help
```

### Usage:

```
# show help
$ python -B ansible_graph.py --help

# run application
$ python -B ansible_graph.py <project> <configuration>
```

or

```
# change chmod
$ chmod u+x ansible_graph.py

# show help
$ ./ansible_graph.py --help

# run application
$ ./ansible_graph.py <project> <configuration>
```

---

## Issues

On some systems (_like Mac OS X_) the Graphviz dot executable is not found (_even the PATH variable is set correct_). The following solution helps to solve.

```
$ which dot
/usr/local/bin/dot

$ vim .env/lib/python2.7/site-packages/graphviz/files.py
```

search and change

```
_engine = 'dot'
```

into

```
_engine = '/usr/local/bin/dot'
```
