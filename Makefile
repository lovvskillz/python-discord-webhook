PACKAGE_NAME=discord_webhook

.PHONY: tests

help:
	@echo 'Usage: make COMMAND'
	@echo
	@echo 'Commands:'
	@echo '    help      Display this message'
	@echo '    format    Run The uncompromising Python code formatter'
	@echo '    lint      Run pylint and flake8'
	@echo '    tests     Run the test suites'

format:
	black discord_webhook/ tests/ -l 88

lint:
	black --check --quiet discord_webhook/ tests/
	pylint --rcfile=.pylintrc $(PACKAGE_NAME)
	flake8 $(PACKAGE_NAME)

tests:
	nosetests
