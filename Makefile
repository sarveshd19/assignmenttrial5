run:
	python main.py

pylint:
	pylint main.py

test:
	coverage run -m pytest
	coverage report main.py