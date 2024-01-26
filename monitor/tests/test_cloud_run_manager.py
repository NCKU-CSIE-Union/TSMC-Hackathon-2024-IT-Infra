from monitor.service.cloudrun import CloudRunManager


def test_cloud_run_manager(cloud_run_manager: CloudRunManager) -> None:
    manager = cloud_run_manager
    assert manager is not None


def test_cloud_run_manager_get_service(cloud_run_manager: CloudRunManager) -> None:
    service_result = cloud_run_manager.get_service("consumer-test")
    assert service_result is not None


def test_cloud_run_manager_adjust_cpu_ram(cloud_run_manager: CloudRunManager) -> None:
    service = cloud_run_manager.get_service("consumer-test")
    assert service is not None

    service = cloud_run_manager.adjust_cpu_ram("consumer-test", 1.0, 600)
    assert service is not None


def test_cloud_run_manager_increase_cpu_ram(cloud_run_manager: CloudRunManager) -> None:
    service = cloud_run_manager.get_service("consumer-test")
    assert service is not None

    service = cloud_run_manager.increase_cpu_ram("consumer-test", 1.0, 600)
    assert service is not None


def test_cloud_run_manager_adjust_instance_count(
    cloud_run_manager: CloudRunManager,
) -> None:
    service = cloud_run_manager.get_service("consumer-test")
    assert service is not None

    service = cloud_run_manager.adjust_instance_count("consumer-test", 1)
    assert service is not None


def test_cloud_run_manager_increase_instance_count(
    cloud_run_manager: CloudRunManager,
) -> None:
    service = cloud_run_manager.get_service("consumer-test")
    assert service is not None

    service = cloud_run_manager.increase_instance_count("consumer-test", 1)
    assert service is not None


# def test_cloud_run_manager_deploy_image(cloud_run_manager : CloudRunManager) -> None:
#     service = cloud_run_manager.get_service("consumer-test")
#     assert service is not None

#     service = cloud_run_manager.deploy_image(service, "gcr.io/tsmccareerhack2024-icsd-grp5/consumer-test:latest")
#     assert service is not None


def test_cloud_run_manager_get_metrics(cloud_run_manager: CloudRunManager) -> None:
    service = cloud_run_manager.get_service("consumer-test")
    assert service is not None

    metrics = cloud_run_manager.get_metrics("consumer-test")
    assert metrics is not None
