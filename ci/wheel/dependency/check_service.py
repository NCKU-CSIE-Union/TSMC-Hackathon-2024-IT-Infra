from google.cloud import run_v2


def check_service(service_id, image_name):
    run_client = run_v2.ServicesClient()
    project_id = "tsmccareerhack2024-icsd-grp5"
    location = "us-central1"

    service_name = f"projects/{project_id}/locations/{location}/services/{service_id}"
    current_service = run_client.get_service(name=service_name)
    print(current_service)


if __name__ == "__main__":
    service_id = "consumer-ci"
    image_name = "us-central1-docker.pkg.dev/tsmccareerhack2024-icsd-grp5/tsmccareerhack2024-icsd-grp5-repository/consumer:latest"

    check_service(service_id, image_name)
