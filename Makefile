start-drones:
	@echo "Starting drones"
	cd ci/setup/drone
	sudo docker compose up -d || docker compose up -d