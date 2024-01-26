start-drones:
	@echo "Starting drones"
	cd ci/setup/drone
	sudo docker compose up -d || docker compose up -d

test-mointor:
	@echo "Starting monitor pytest"
	coverage run -m pytest monitor/tests
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

	

