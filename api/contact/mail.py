import boto3
from users.keys import *

def send_mail(destination,sender,name,email,mobile,message):
    client = boto3.client('ses',aws_access_key_id=AWS_ACCESS_KEY,
        aws_secret_access_key=AWS_SECRET_KEY,
        region_name=AWS_REGION)
    response = client.send_email(
        Destination={
            'ToAddresses': [
                destination
            ],
        },
        Message={
        'Body': {
            'Html': {
            'Charset': 'UTF-8',
            'Data': '''<h1>Contact Enquiry from {name}</h1>
            <p>Email: {email}</p>
            <p>Phone Number: {mobile}</p>
            <p>Message: {message}</p>'''.format(name=name,email=email,mobile=mobile,message=message),
            },
                'Text': {
                    'Charset': 'UTF-8',
                    'Data': 'This is for those who cannot read HTML.',
                },
            },
            'Subject': {
                'Charset': 'UTF-8',
                'Data': 'Enquiry',
            },
        },
        Source=sender,
    )
    return response
