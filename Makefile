format:
	black ./**/*.py
	isort ./**/*.py

lint:
	flake8 ./**/*.py