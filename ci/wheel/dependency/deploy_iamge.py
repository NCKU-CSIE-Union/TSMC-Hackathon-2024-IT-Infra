from google.cloud import run_v2


def deploy_image(service_id, image_name):
    run_client = run_v2.ServicesClient()
    project_id = "tsmccareerhack2024-icsd-grp5"
    location = "us-central1"

    service_name = f"projects/{project_id}/locations/{location}/services/{service_id}"
    current_service = run_client.get_service(name=service_name)
    print(current_service)

    current_service.template.containers[0].image = image_name
    # if you want to set all container to use the same image, uncomment the following two lines
    # for container in current_service.template.containers:
    #     container.image = image
    request = run_v2.UpdateServiceRequest(service=current_service)

    operation = run_client.update_service(request=request)

    response = operation.result()  # Blocks until operation is complete
    return response


if __name__ == "__main__":
    service_id = "consumer-ci"
    image_name = "us-central1-docker.pkg.dev/tsmccareerhack2024-icsd-grp5/tsmccareerhack2024-icsd-grp5-repository/consumer:latest"

    deploy_image(service_id, image_name)
