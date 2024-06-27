up:
	podman-compose up -d
down:
	podman-compose down
test:
	pytest tests/
install:
	poetry install
shell:
	poetry shell
style:
	flake8 .
style-fix:
	black .