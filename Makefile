run:
	python main.py

pylint:
	pylint main.py

test:
	coverage run -m pytest
	coverage report main.py

db:
	alembic upgrade fd9cf0389ab2