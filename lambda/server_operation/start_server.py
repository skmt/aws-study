import boto3


def lambda_handler(event, context):
    start_instance()


def start_instance():
    ec2 = boto3.resource('ec2').Instance('i-AAAAAAAAAAAAAAAAAA')
    ec2.start()
    ec2.wait_until_running()
    return
