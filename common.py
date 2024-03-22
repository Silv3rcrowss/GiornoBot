import json
import boto3
from botocore.exceptions import ClientError
from typing import Optional


def get_secret(secret_name, region_name) -> Optional[dict]:
    """
    Retrieves a secret from AWS Secrets Manager
    :param secret_name: The name of the secret
    :param region_name: The AWS region where the secret is stored
    :return: The secret as a dictionary
    """
    session = boto3.session.Session()
    client = session.client(
        service_name="secretsmanager",
        region_name=region_name,
    )

    try:
        response = client.get_secret_value(SecretId=secret_name)
    except ClientError as error:
        print(f"Error retrieving secret: {error}")
        return None

    return json.loads(response["SecretString"])


def get_parameter(parameter_name, region_name) -> Optional[dict]:
    """
    Retrieves a parameter  from AWS Systems Manager
    :param parameter_name: The name of the secret
    :param region_name: The AWS region where the secret is stored
    :return: The parameter as a dictionary
    """
    session = boto3.session.Session()
    client = session.client(
        service_name="ssm",
        region_name=region_name,
    )

    try:
        response = client.get_parameter(Name=parameter_name, WithDecryption=True)
    except ClientError as error:
        print(f"Error retrieving parameter: {error}")
        return None
    return response["Parameter"]["Value"]
