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
	python_version_full := $(wordlist 2,4,$(subst ., ,$(shell $(PYTHON) --version 2>&1)))
    python_version_major := $(word 1,${python_version_full})
    python_version_minor := $(word 2,${python_version_full})

    VER_GE_3_5 := $(shell [ $(python_version_major) -gt 3 -o \( $(python_version_major) -eq 3 -a $(python_version_minor) -ge 10 \) ] && echo true)

    ifeq ($(VER_GE_3_5),true)
		XPYTHON=$(PYTHON)
    endif
endif

ifndef XPYTHON
ifdef PYTHON3_EXISTS
	python_version_full := $(wordlist 2,4,$(subst ., ,$(shell $(PYTHON3) --version 2>&1)))
    python_version_major := $(word 1,${python_version_full})
    python_version_minor := $(word 2,${python_version_full})

	VER_GE_3_5 := $(shell [ $(python_version_major) -gt 3 -o \( $(python_version_major) -eq 3 -a $(python_version_minor) -ge 10 \) ] && echo true)

	ifeq ($(VER_GE_3_5),true)
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
