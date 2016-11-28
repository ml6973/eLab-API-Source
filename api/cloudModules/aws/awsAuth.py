import boto3


def authClient(ACCESS_KEY,SECRET_KEY,REGION):
    client=boto3.client('ec2',
                          aws_access_key_id=ACCESS_KEY,
                          aws_secret_access_key=SECRET_KEY,
			  region_name=REGION
			  )
    return client


def authResource(ACCESS_KEY,SECRET_KEY,REGION):
    resource = boto3.resource('ec2',
                              aws_access_key_id=ACCESS_KEY,
			      aws_secret_access_key=SECRET_KEY,
			      region_name=REGION)
    return resource
