pre-init:
	python ./scripts/pre_init.py

daemon:
	docker-compose up -d

post-init:
	python ./scripts/post_init.py

update-all:
	docker-compose down || true
	python ./scripts/pre_init.py false
	docker-compose up -d
	python ./scripts/post_init.py

py3-update-all:
	docker-compose down || true
	python3 ./scripts/pre_init.py false
	docker-compose up -d
	python3 ./scripts/post_init.py
