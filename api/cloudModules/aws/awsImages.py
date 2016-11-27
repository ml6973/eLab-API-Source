import boto3


def getImageList(client):
    images = client.describe_images(Owners=['self'])["Images"]
    return images
