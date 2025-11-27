import boto3
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    logger.info(f"Recieved Event : {event}")
    try:
        instance_id = event.get("existing_instance_id")
        ec2_client = boto3.client("ec2", region_name="us-east-1")
        resp = ec2_client.create_image(
            Description=f"AMI from an existing instance with id {instance_id}",
            InstanceId=instance_id,
            Name="Assignment3-AMI",
            NoReboot=True
        )
        logger.info(f"AMI created : {resp.get("ImageId")}")
        return {
            "AMI_id": resp.get("ImageId")
        }
    except Exception as e:
        logger.error(e)
        raise e