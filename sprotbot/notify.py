
import boto3
import os

def get_aws_creds():
    """
    Pulls the AWS credentials from the current environment.
    This assumes the following two environment variables are set:

        - AWS_ACCESS_KEY_ID -- the public part of the AWS credential
        - AWS_SECRET_ACCESS_KEY -- the private part of the AWS credential

    It is also assumed that the AWS account to which these credentials belong
    has write access to the SES service.
    """

    try:
        key_id = os.environ["AWS_ACCESS_KEY_ID"]
        key_secret = os.environ["AWS_SECRET_ACCESS_KEY"]
    except KeyError as ex:
        raise AWSCredentialsError("AWS credentials not available in environment variables.")

    return key_id, key_secret

class AWSCredentialsError(Exception):
    pass

def send_email(sender, recipient, subject, message):
    """
    Sends an email to a single recipient with a given subject and message.

    Addresses can be formatted according to the pattern:
      "Joe Bloggs <joe.bloggs@example.net>"

    Message sent as plain text.

    Assumptions:
      1. sender needs to be verified in AWS.
      2. if recipient not verified, then AWS account must not be in SES Sandbox.
    """

    access_id, access_secret = get_aws_creds()

    client = boto3.client("ses",
                          aws_access_key_id = access_id,
                          aws_secret_access_key = access_secret)

    client.send_email(Source=sender,
                      Destination={"ToAddresses": [recipient]},
                      Message={"Subject": {"Data": subject},
                               "Body": {"Text": {"Data": message}}})
