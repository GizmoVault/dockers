PYTHON=python
PYTHON3=python3

ifneq (, $(shell which $(PYTHON) ))
	PYTHON_EXISTS=1
endif

ifneq (, $(shell which $(PYTHON3) ))
	PYTHON3_EXISTS=1
endif

ifndef PYTHON_EXISTS
ifndef PYTHON3_EXISTS
	$(error "PYTHON=$(PYTHON) OR PYTHON=$(PYTHON3) not found in $(PATH)")
endif
endif

ifdef PYTHON_EXISTS
	PYTHON_VERSION_MIN=3.5
	PYTHON_VERSION=$(shell $(PYTHON) -c 'import sys; print("%d.%d"% sys.version_info[0:2])' )
	PYTHON_VERSION_OK=$(shell $(PYTHON) -c 'import sys;\
	  print(int(float("%d.%d"% sys.version_info[0:2]) >= $(PYTHON_VERSION_MIN)))' )

	ifneq ($(PYTHON_VERSION_OK),0)
	  XPYTHON=$(PYTHON)
	endif
endif

ifndef XPYTHON
ifdef PYTHON3_EXISTS
	PYTHON_VERSION_MIN=3.5
	PYTHON_VERSION=$(shell $(PYTHON3) -c 'import sys; print("%d.%d"% sys.version_info[0:2])' )
	PYTHON_VERSION_OK=$(shell $(PYTHON3) -c 'import sys;\
	  print(int(float("%d.%d"% sys.version_info[0:2]) >= $(PYTHON_VERSION_MIN)))' )

	ifneq ($(PYTHON_VERSION_OK),0)
	  XPYTHON=$(PYTHON3)
	endif
endif
endif

ifndef XPYTHON
	$(error "no matched ptyhon found")
endif

ifeq (, $(shell which docker-compose ))
	DOCKER_COMPOSE=docker compose
else
	DOCKER_COMPOSE=docker-compose
endif

check:
	$(XPYTHON) --version
	$(DOCKER_COMPOSE) version

re-init:
	$(XPYTHON) ./scripts/pre_init.py

daemon:
	$(DOCKER_COMPOSE) up -d

post-init:
	$(XPYTHON) ./scripts/post_init.py

update-all:
	@if [ -e docker-compose.yaml ]; then $(DOCKER_COMPOSE) down; fi
	$(XPYTHON) ./scripts/pre_init.py false
	$(DOCKER_COMPOSE) up -d
	$(XPYTHON) ./scripts/post_init.py
	$(DOCKER_COMPOSE) restart
