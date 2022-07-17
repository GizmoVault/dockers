pre-init:
	python ./scripts/pre_init.py

daemon:
	docker-compose up -d

post-init:
	python ./scripts/post_init.py

update-all:
	@if [ -e docker-compose.yaml ]; then docker-compose down; fi
	python ./scripts/pre_init.py false
	docker-compose up -d
	python ./scripts/post_init.py
	docker-compose restart

py3-update-all:
	@if [ -e docker-compose.yaml ]; then docker-compose down; fi
	python3 ./scripts/pre_init.py false
	docker-compose up -d
	python3 ./scripts/post_init.py
	docker-compose restart

update-all-2:
	@if [ -e docker-compose.yaml ]; then docker compose down; fi
	python ./scripts/pre_init.py false
	docker compose up -d
	python ./scripts/post_init.py
	docker compose restart

py3-update-all-2:
	@if [ -e docker-compose.yaml ]; then docker compose down; fi
	python3 ./scripts/pre_init.py false
	docker compose up -d
	python3 ./scripts/post_init.py
	docker compose restart
