up:
	podman-compose up -d
down:
	podman-compose down
test:
	pytest tests/
install:
	poetry install
