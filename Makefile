ENV_DIR = .env

help:
	@echo "Run make <target> with:"
	@echo " > env           : create virtualenv on folder $(ENV_DIR)"
	@echo " > deps          : install dependentcies"
	@echo " > lint          : run pylint"
	@echo " > bandit        : run bandit"
	@echo " > cleanenv      : delete virtualenv"

env:
	virtualenv $(ENV_DIR) \
	&& . $(ENV_DIR)/bin/activate \
	&& make deps

deps:
	$(ENV_DIR)/bin/pip install -r requirements.txt

lint:
	$(ENV_DIR)/bin/pylint ansible_stats.py

bandit:
	$(ENV_DIR)/bin/bandit -r ansible_statistics/

cleanenv:
	rm -fr $(ENV_DIR)
