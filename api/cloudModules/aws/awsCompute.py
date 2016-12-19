import boto3


def boot_vm(resource, name, imageid):
    with open('cfg.sh', 'r') as configfile:
        config = configfile.read()
    new_instance = resource.create_instances(
					     ImageId=imageid,
					     MinCount=1,
					     MaxCount=1,
					     InstanceType='t2.micro',
					     UserData=config,
					     SecurityGroupIds=['sg-8d9bb4f4']
					     )
    instance = new_instance[0]

    # Wait for the instance to enter the running state
    instance.wait_until_running()

    # Reload instance attributes
    instance.load()

    # Set instance tag values
    instance.create_tags(Tags=[
                               {
			        "Key": "Name",
			        "Value": name
			       }
			      ]
			 )

    print instance
    return instance.instance_id



def get_IP(resource, computeId):
    instance = resource.Instance(computeId)
    return instance.public_ip_address


def delete_vm(resource, computeId):
   instance = resource.Instance(computeId)
   instance.terminate()

   #Wait for instance to be terminated
   instance.wait_until_terminated()
