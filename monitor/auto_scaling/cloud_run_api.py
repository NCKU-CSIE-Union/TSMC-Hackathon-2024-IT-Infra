import time

from google.cloud import monitoring_v3, run_v2

project_id = "tsmccareerhack2024-icsd-grp5"
project_name = f"projects/{project_id}"


class CloudRunManager:
    def __init__(
        self,
        run_client: run_v2.ServicesClient,
        monitoring_client: monitoring_v3.MetricServiceClient,
    ):
        self.cloud_run_client = run_client
        self.monitoring_client = monitoring_client

    def adjust_cpu_ram(self, instance_id, cpu=None, ram=None):
        """
        Adjusts the CPU and RAM of a cloud instance.

        :param instance_id: ID of the instance to adjust.
        :param cpu: New CPU configuration.
        :param ram: New RAM configuration.
        """
        # https://github.com/googleapis/google-cloud-python/blob/main/packages/google-cloud-run/google/cloud/run_v2/types/service.py#L502
        # https://github.com/googleapis/google-cloud-python/blob/main/packages/google-cloud-run/google/cloud/run_v2/types/revision_template.py#L144
        # https://github.com/googleapis/google-cloud-python/blob/main/packages/google-cloud-run/google/cloud/run_v2/types/k8s_min.py#L164
        request = run_v2.UpdateServiceRequest(
            service=run_v2.Service(
                name=instance_id,
                template=run_v2.RevisionTemplate(
                    containers=[
                        run_v2.Container(
                            resources=run_v2.ResourceRequirements(
                                limits={"cpu": cpu, "memory": ram}
                            )
                        )
                    ]
                ),
            )
        )

        operation = self.cloud_run_client.update_service(request=request)

        response = operation.result()  # Blocks until operation is complete
        return response

    def adjust_instance_count(self, instance_id, new_count):
        """
        Adjusts the number of running instances.

        :param new_count: The target number of instances.
        """
        # https://github.com/googleapis/google-cloud-python/blob/main/packages/google-cloud-run/google/cloud/run_v2/types/service.py#L502
        # https://github.com/googleapis/google-cloud-python/blob/main/packages/google-cloud-run/google/cloud/run_v2/types/revision_template.py#L33
        # https://github.com/googleapis/google-cloud-python/blob/313f5672c1d16681dd4db2c4a995c5668259ea7d/packages/google-cloud-run/google/cloud/run_v2/types/vendor_settings.py#L213
        request = run_v2.UpdateServiceRequest(
            service=run_v2.Service(
                name=instance_id,
                template=run_v2.RevisionTemplate(
                    scale=run_v2.RevisionScaling(
                        min_instance_count=new_count, max_instance_count=new_count
                    )
                ),
            )
        )

        operation = self.cloud_run_client.update_service(request=request)

        response = operation.result()  # Blocks until operation is complete
        return response

    def deploy_image(self, drone_id, image):
        # self.client.
        """
        Deploys a new image to a cloud run.

        :param image: The new image to deploy.
        """
        request = run_v2.UpdateServiceRequest(
            service=run_v2.Service(
                name=drone_id,
                template=run_v2.RevisionTemplate(
                    containers=[
                        run_v2.Container(
                            image=image,
                        )
                    ]
                ),
            )
        )

        operation = self.cloud_run_client.update_service(request=request)

        response = operation.result()  # Blocks until operation is complete
        return response

    def get_metrics(
        self,
        instance_name,
        start_time=int(time.time() - 60 * 60 * 3),
        end_time=int(time.time()),
    ):
        """
        Gets the metrics of a cloud run.

        :param drone_id: The ID of the cloud run.
        """

        # TODO: currently only gets CPU utilization, add more metrics
        return self.monitoring_client.list_time_series(
            request=monitoring_v3.ListTimeSeriesRequest(
                name=f"projects/{project_id}",
                filter=f'metric.type="run.googleapis.com/container/cpu/utilizations" AND resource.label."configuration_name"="{instance_name}"',
                aggregation=monitoring_v3.Aggregation(
                    alignment_period={"seconds": 60},
                    per_series_aligner=monitoring_v3.Aggregation.Aligner.ALIGN_DELTA,
                    cross_series_reducer=monitoring_v3.Aggregation.Reducer.REDUCE_MEAN,
                ),
                interval=monitoring_v3.TimeInterval(
                    {
                        "start_time": {"seconds": int(start_time)},
                        "end_time": {"seconds": int(end_time)},
                    }
                ),
            ),
        )


if __name__ == "__main__":
    monitoring_client = monitoring_v3.MetricServiceClient()
    run_manager = CloudRunManager(
        run_v2.ServicesClient(), monitoring_v3.MetricServiceClient()
    )

    metric = run_manager.get_metrics("consumer")
    print(metric)
