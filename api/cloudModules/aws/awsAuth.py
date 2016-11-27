import boto3


def auth(ACCESS_KEY,SECRET_KEY,REGION):
    client=boto3.client('ec2',
                          aws_access_key_id=ACCESS_KEY,
                          aws_secret_access_key=SECRET_KEY,
			  region_name=REGION
			  )
    return client
