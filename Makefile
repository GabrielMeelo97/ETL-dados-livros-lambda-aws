## CI/CD
ci-setup:
	pip install poetry
	poetry install
	npm install -g serverless && npm install serverless-python-requirements serverless-pseudo-parameters
	npm install --save-dev serverless-plugin-warmup serverless-prune-plugin