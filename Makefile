start-drones:
	@echo "Starting drones"
	cd ci/setup/drone
	@docker compose up -d