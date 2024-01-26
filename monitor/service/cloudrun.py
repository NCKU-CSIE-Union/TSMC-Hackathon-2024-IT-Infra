import datetime
import logging
import random
import time

import pandas as pd
from google.cloud import monitoring_v3, run_v2
from pydantic import BaseModel


class CloudRunManager:
    def __init__(
        self,
        run_client: run_v2.ServicesClient = run_v2.ServicesClient(),
        monitoring_client: monitoring_v3.MetricServiceClient = monitoring_v3.MetricServiceClient(),
        project_id="tsmccareerhack2024-icsd-grp5",
        location="us-central1",
    ):
        self.cloud_run_client = run_client
        self.monitoring_client = monitoring_client
        self.project_id = project_id
        self.project_name = f"projects/{project_id}"
        self.location = location

    def get_service(self, service_id):
        """
        Gets the configuration of a cloud run.

        :param service_id: The name of the cloud run which you named it in the create form. (e.g. consumer)
        """
        service_name = f"projects/{self.project_id}/locations/{self.location}/services/{service_id}"
        return self.cloud_run_client.get_service(name=service_name)

    def adjust_cpu_ram(self, service_id, cpu: float, ram: float, ram_unit="M"):
        """
        Adjusts the CPU and RAM of a cloud instance.

        :param service_id: The name of the cloud run which you named it in the create form. (e.g. consumer)
        :param cpu: New CPU configuration.
        :param ram: New RAM configuration.
        :param ram_unit (optional): The unit of RAM. (e.g. M, G)
        """
        service_name = f"projects/{self.project_id}/locations/{self.location}/services/{service_id}"
        # Retrieve the current configuration of the service
        current_service = self.cloud_run_client.get_service(name=service_name)
        # Modify only the resource requirements
        for container in current_service.template.containers:
            container.resources = run_v2.ResourceRequirements()
            container.resources.limits = {
                "cpu": f"{cpu}",
                "memory": f"{ram}{ram_unit}",
            }
        # Update the service with the modified configuration
        request = run_v2.UpdateServiceRequest(service=current_service)

        operation = self.cloud_run_client.update_service(request=request)
        print("Updating service with new CPU and RAM ...")

        try:
            response: run_v2.Service = operation.result(timeout=30)  # noqa: F841
            return True
        except Exception:
            return False

    def increase_cpu_ram(
        self, service_id, cpu_delta: float = 0, ram_delta: int = 0, ram_unit="M"
    ):
        """
        Adjusts the CPU and RAM of a cloud instance.

        :param service_id: The name of the cloud run which you named it in the create form. (e.g. consumer)
        :param cpu_delta: The Delta of current CPU configuration. (unit: no unit, number only, e.g. 1, 69, 420)
        :param ram_delta: The Delta of current RAM configuration. (unit: MB)
        :param ram_unit (optional): The unit of RAM. (e.g. M, G)
        """
        service_name = f"projects/{self.project_id}/locations/{self.location}/services/{service_id}"
        current_service = self.cloud_run_client.get_service(name=service_name)
        # Modify the resource requirements
        for container in current_service.template.containers:
            original_cpu = container.resources.limits["cpu"]
            original_ram = container.resources.limits["memory"]
            try:
                original_cpu = float(
                    "".join(c for c in original_cpu if c.isdigit() or c == ".")
                )
            except Exception:
                original_cpu = 0
            try:
                original_ram = int(
                    "".join(c for c in original_ram if c.isdigit() or c == ".")
                )
            except Exception:
                original_ram = 0
            container.resources = run_v2.ResourceRequirements()
            new_cpu = (
                (original_cpu + cpu_delta) > 1 and int(original_cpu + cpu_delta) or 0.5
            )
            new_ram = original_ram + ram_delta
            container.resources.limits = {
                "cpu": f"{new_cpu}",
                "memory": f"{new_ram}{ram_unit}",
            }
            print(
                f"Container {container.name} CPU: {new_cpu}, RAM: {new_ram}{ram_unit}"
            )
        # Update the service with the modified configuration
        request = run_v2.UpdateServiceRequest(service=current_service)

        # Wait for the operation to complete
        operation = self.cloud_run_client.update_service(request=request)
        print("Updating service with new CPU and RAM ...")

        try:
            response: run_v2.Service = operation.result(timeout=30)  # noqa: F841
            return True
        except Exception:
            return False

    def adjust_instance_count(self, service_id: str, new_count: int):
        """
        Adjusts the number of running instances.

        :param service_id: The name of the cloud run which you named it in the create form. (e.g. consumer)
        :param new_count: The target number of instances.
        """

        service_name = f"projects/{self.project_id}/locations/{self.location}/services/{service_id}"
        # Retrieve the current configuration of the service
        current_service = self.cloud_run_client.get_service(name=service_name)

        # Modify only the scaling parameters
        current_service.template.scaling.min_instance_count = new_count
        current_service.template.scaling.max_instance_count = new_count

        for container in current_service.template.containers:
            container.env = [
                run_v2.EnvVar(
                    name="CURRENT_INSTANCE_COUNT",
                    value=f"{new_count}",
                ),
            ]
        request = run_v2.UpdateServiceRequest(service=current_service)

        operation = self.cloud_run_client.update_service(request=request)
        print(f"Updating service with new instance count: {new_count} ...")
        try:
            response: run_v2.Service = operation.result(  # noqa: F841
                timeout=30
            )  # Blocks until operation is complete
            return True

        except Exception:
            return False

    def increase_instance_count(self, service_id: str, delta: int):
        """
        Adjusts the number of running instances.

        :param service_id: The name of the cloud run which you named it in the create form. (e.g. consumer)
        :param delta: The delta of the number of instances.
        """

        service_name = f"projects/{self.project_id}/locations/{self.location}/services/{service_id}"
        # Retrieve the current configuration of the service
        current_service = self.cloud_run_client.get_service(name=service_name)
        new_count = current_service.template.scaling.min_instance_count + delta
        # Modify only the scaling parameters
        current_service.template.scaling.min_instance_count = new_count
        current_service.template.scaling.max_instance_count = new_count

        for container in current_service.template.containers:
            container.env = [
                run_v2.EnvVar(
                    name="CURRENT_INSTANCE_COUNT",
                    value=f"{current_service.template.scaling.min_instance_count}",
                ),
            ]
        request = run_v2.UpdateServiceRequest(service=current_service)

        operation = self.cloud_run_client.update_service(request=request)
        print(f"Updating service with new instance count: {new_count} ...")
        try:
            response: run_v2.Service = operation.result(  # noqa: F841
                timeout=30
            )  # Blocks until operation is complete
            return True

        except Exception:
            return False

    def deploy_image(self, service_id, image):
        """
        Deploys a new image to a cloud run.

        :param image: The new image to deploy.
        """
        # Retrieve the current configuration of the service
        service_name = f"projects/{self.project_id}/locations/{self.location}/services/{service_id}"
        current_service = self.cloud_run_client.get_service(name=service_name)

        current_service.template.containers[0].image = image
        request = run_v2.UpdateServiceRequest(service=current_service)

        operation = self.cloud_run_client.update_service(request=request)

        response = operation.result()  # Blocks until operation is complete
        return response

    def get_metrics(
        self,
        service_id: str,
        start_time=int(time.time() - 60 * 60 * 3),
        end_time=int(time.time()),
    ):
        # TODO: Add Request Count (1xx),Request Count (2xx),Request Count (3xx),Request Count (4xx)
        # TODO: Request Latency (ms)
        class MetricReflectName(BaseModel):
            class Config:
                arbitrary_types_allowed = True

            column_name: str
            metric_name: str
            aggregation: monitoring_v3.Aggregation = monitoring_v3.Aggregation(
                alignment_period={"seconds": 60},
                per_series_aligner=monitoring_v3.Aggregation.Aligner.ALIGN_DELTA,
                cross_series_reducer=monitoring_v3.Aggregation.Reducer.REDUCE_MEAN,
            )

        metric_filters = [
            MetricReflectName(
                column_name="Container CPU Utilization (%)",
                metric_name="run.googleapis.com/container/cpu/utilizations",
            ),
            MetricReflectName(
                column_name="Container Memory Utilization (%)",
                metric_name="run.googleapis.com/container/memory/utilizations",
            ),
            MetricReflectName(
                column_name="Instance Count",
                metric_name="run.googleapis.com/container/instance_count",
                aggregation=monitoring_v3.Aggregation(
                    alignment_period={"seconds": 60},
                    per_series_aligner=monitoring_v3.Aggregation.Aligner.ALIGN_MEAN,
                    cross_series_reducer=monitoring_v3.Aggregation.Reducer.REDUCE_NONE,
                ),
            ),
        ]
        data = []
        for metric in metric_filters:
            # print(f"Getting metric: {metric.metric_name}")
            response = self.monitoring_client.list_time_series(
                request=monitoring_v3.ListTimeSeriesRequest(
                    name=f"projects/{self.project_id}",
                    filter=f'metric.type="{metric.metric_name}" AND resource.label."configuration_name"="{service_id}"',
                    aggregation=metric.aggregation,
                    interval=monitoring_v3.TimeInterval(
                        {
                            "start_time": {"seconds": int(start_time)},
                            "end_time": {"seconds": int(end_time)},
                        }
                    ),
                ),
            )
            for series in response:
                for point in series.points:
                    if "Instance Count" in metric.column_name:
                        metric.column_name = (
                            f"Instance Count ({series.metric.labels['state']})"
                        )
                    data.append(
                        {
                            "Time": datetime.datetime.fromtimestamp(
                                point.interval.end_time.timestamp(),
                                datetime.timezone.utc,
                            ),
                            metric.column_name: point.value.double_value,
                        }
                    )

        metric_df: pd.DataFrame = pd.DataFrame(data)
        metric_df = metric_df.groupby("Time").first().reset_index()
        metric_df = metric_df.sort_values(by="Time", ascending=True)

        # convert to percentage
        metric_df["Container CPU Utilization (%)"] = (
            metric_df["Container CPU Utilization (%)"] * 100
        )
        metric_df["Container Memory Utilization (%)"] = (
            metric_df["Container Memory Utilization (%)"] * 100
        )

        # fill missing columns with time interpolation
        metric_df.set_index("Time", inplace=True)
        metric_df = metric_df.interpolate(method="time")
        metric_df.reset_index(inplace=True)

        return metric_df


if __name__ == "__main__":
    project_id = "tsmccareerhack2024-icsd-grp5"
    location = "us-central1"
    monitoring_client = monitoring_v3.MetricServiceClient()
    run_manager = CloudRunManager(
        run_client=run_v2.ServicesClient(),
        monitoring_client=monitoring_v3.MetricServiceClient(),
        project_id=project_id,
        location=location,
    )

    # run_manager.increase_cpu_ram("consumer", cpu_delta=1, ram_delta=69)
    # run_manager.increase_instance_count("consumer", 69)

    metric = run_manager.get_metrics("consumer-sentry")
    print(metric)
    exit()
    # print(metric)
    while True:
        command = input("Enter command: ")
        if command == "adjust cpu":
            desired_cpu = random.choice([0.5, 1, 2, 4, 6, 8])
            desired_ram = random.randint(2000, 10000)
            print(
                f"Adjusting CPU to {desired_cpu} and RAM to {desired_ram} for consumer"
            )
            print(
                run_manager.adjust_cpu_ram(
                    "consumer",
                    cpu=desired_cpu,
                    ram=desired_ram,
                )
            )
        elif command == "deploy image":
            print(
                run_manager.deploy_image(
                    "consumer", "gcr.io/tsmccareerhack2024-icsd-grp5/consumer:latest"
                )
            )
        elif command == "scale up":
            desired_count = random.randint(1, 5)
            print(f"Scaling instance count to {desired_count} for consumer")
            res = run_manager.adjust_instance_count("consumer", desired_count)
            if res is None:
                print("Failed to scale up")
            else:
                print("Successfully scaled up")
        elif command == "scale down":
            print("Scaling instance count to 0 for consumer")
            print(run_manager.adjust_instance_count("consumer", 0))
        elif command == "exit":
            break
        else:
            logging.warn("Invalid command")
