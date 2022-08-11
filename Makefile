clean : ## Remove residual files
	rm -rfv **/__pycache__
	rm -rfv *.egg-info
	rm -rfv .pytest_cache
	rm -rfv .tox
	rm -rfv *.pyc
	rm -rfv *.pyd
	rm -rfv dist
	rm -rfv build
	rm -rfv htmlcov
	rm -rfv coverage.xml
	rm -rfv .coverage

test : clean ## Run Unittests
	pytest --cov=ebookatty --cov=tests --ff
	coverage xml -o coverage.xml
	coverage html
	coverage report
