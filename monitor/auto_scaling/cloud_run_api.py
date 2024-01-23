from google.cloud import run_v2


class CloudRunManager:
    def __init__(self, client: run_v2.ServicesClient):
        self.client = client

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

        operation = self.client.update_service(request=request)

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

        operation = self.client.update_service(request=request)

        response = operation.result()  # Blocks until operation is complete
        return response

    def deploy_image(self, drone_id, image):
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

        operation = self.client.update_service(request=request)

        response = operation.result()  # Blocks until operation is complete
        return response


# Example usage
# adjust_cpu_ram('instance123', cpu='2 vCPUs', ram='4 GB')
# adjust_instance_count(5)
# deploy_image('new_image_version')
