import boto3
import logging
from time import sleep

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    logger.info(f"Received event: {event}")
    try:
        ami_id = event.get('AMI_id')
        ec2_client = boto3.client('ec2', region_name="us-east-1")

        img_status = None # status of the AMI image
        while img_status != "available":
            # Wait until the AMI becomes available to launch the instance
            sleep(15)
            resp = ec2_client.describe_images(
                ImageIds=[ami_id]
            )
            img_status = resp["Images"][0]["State"]
            logger.info(f"AMI status: {img_status}")

        resp = ec2_client.run_instances(
            ImageId=ami_id,
            InstanceType="t3.micro",
            MinCount=1,
            MaxCount=1,
            TagSpecifications=[
                {
                    "ResourceType": "instance",
                    "Tags": [
                        {
                            "Key": "Name",
                            "Value": "Assignment3-instance-from-AMI"
                        }
                    ]
                }
            ]
        )
        logger.info(f"Instance launched: {resp}")
        return {
            "Instance_id": resp["Instances"][0]["InstanceId"]
        }
    except Exception as e:
        logger.error(f"Error: {e}")
        raise e