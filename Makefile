start-drones:
	@echo "Starting drones"
	cd ci/setup/drone
	docker  compose up -d || docker compose up -d

test-mointor:
	@echo "Starting monitor pytest"
	coverage run -m pytest monitor/tests
	@echo "Generating coverage report"
	coverage report -m
	coverage html

test-llm-analyzer:
	@echo "Starting monitor pytest"
	coverage run -m pytest ai2/tests
	@echo "Generating coverage report"
	coverage report -m
	coverage html

test-mointor-cloud-run-manager:
	@echo "Starting `cloud_run_manager` Test"
	coverage run -m pytest monitor/tests/test_cloud_run_manager.py
	@echo "Generating coverage report"
	coverage report -m
	coverage html

test-mointor-conversation-manager:
	@echo "starting `conversation_manager` Test"
	coverage run -m pytest monitor/tests/test_conversation_manager.py
	@echo "Generating coverage report"
	coverage report -m
	coverage html

test-bot:
	@echo "Starting bot pytest"
	coverage run -m pytest bot/tests
	@echo "Generating coverage report"
	coverage report -m
	coverage html

build-main-mac:
	@echo "Building main"
	docker build -t jasonbigcow/tsmc_main:mac . 


build-main-linux:
	@echo "Building main"
	docker build -t jasonbigcow/tsmc_main:linux --platform linux/amd64 . 

run-main-mac:
	@echo "Starting main"
	docker compose up -f docker-compose-mac.yml

run-main-linux:
	@echo "Starting main"
	docker compose up -f docker-compose.yml

	

